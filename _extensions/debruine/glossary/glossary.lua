-- Glossary.lua (rewritten for Quarto book PDF + HTML)
-- Based on original by Lisa DeBruine

-- Global state (persists across chapters in PDF book mode)
globalGlossaryDefinitions = {}
globalTermsSeen = {}
glossaryLoaded = false

-- Helper: check if a key exists in kwargs
local function kwExists(kwargs, keyword)
    for key, _ in pairs(kwargs) do
        if key == keyword then return true end
    end
    return false
end

-- Helper: merge default options with meta and user-provided kwargs
local function mergeOptions(userOptions, meta)
  local defaultOptions = {
    path = "glossary.yml",
    popup = "hover",
    show = true,
    add_to_table = true
  }
  if meta.glossary ~= nil then
    for k, v in pairs(meta.glossary) do
      local value = pandoc.utils.stringify(v)
      if value == 'true' then value = true end
      if value == 'false' then value = false end
      defaultOptions[k] = value
    end
  end
  if userOptions ~= nil then
    for k, v in pairs(userOptions) do
      local value = pandoc.utils.stringify(v)
      if value == 'true' then value = true end
      if value == 'false' then value = false end
      defaultOptions[k] = value
    end
  end
  return defaultOptions
end

-- Helper: load glosario.yml into globalGlossaryDefinitions (once per Lua env)
local function loadGlossaryOnce(options)
  if glossaryLoaded then return end
  local metafile = io.open(options.path, 'r')
  if metafile then
    local content = "---\n" .. metafile:read("*a") .. "\n---\n"
    metafile:close()
    local glossary = pandoc.read(content, "markdown").meta
    for key, value in pairs(glossary) do
      globalGlossaryDefinitions[string.lower(key)] = pandoc.utils.stringify(value)
    end
    glossaryLoaded = true
  end
end

-- Helper: return sorted list of keys
local function sortByKeys(tbl)
    local sortedKeys = {}
    for key, _ in pairs(tbl) do
        table.insert(sortedKeys, key)
    end
    table.sort(sortedKeys)
    return sortedKeys
end

-- Helper: add CSS dependency for HTML
local function addHTMLDeps()
  quarto.doc.add_html_dependency({
    name = 'glossary',
    stylesheets = {'glossary.css'}
  })
end

-- Helper: escape special LaTeX characters
local function escapeLaTeX(str)
  if not str then return "" end
  local map = {
    ["#"] = "\\#",
    ["$"] = "\\$",
    ["%"] = "\\%",
    ["&"] = "\\&",
    ["_"] = "\\_",
    ["{"] = "\\{",
    ["}"] = "\\}",
    ["~"] = "\\textasciitilde{}",
    ["^"] = "\\textasciicircum{}",
    ["\\"] = "\\textbackslash{}"
  }
  -- Escape backslash first to avoid escaping the escapes
  str = str:gsub("\\", "!!MAGIC_BS!!")
  str = str:gsub("([#$%&_{}~^])", function(c) return map[c] end)
  str = str:gsub("!!MAGIC_BS!!", "\\textbackslash{}")
  return str
end

-- Main shortcode handler
return {
  ["glossary"] = function(args, kwargs, meta)
    local options = mergeOptions(kwargs, meta)
    loadGlossaryOnce(options)

    -- ── Table mode ─────────────────────────────────────────────────────────
    if kwExists(kwargs, "table") then
      local sortedKeys = sortByKeys(globalGlossaryDefinitions)

      if quarto.doc.isFormat("html:js") then
        addHTMLDeps()
        local gt = "<table class='glossary_table'>\n<tr><th>Término</th><th>Definición</th></tr>\n"
        for _, key in ipairs(sortedKeys) do
          gt = gt .. "<tr><td>" .. key .. "</td><td>" .. globalGlossaryDefinitions[key] .. "</td></tr>\n"
        end
        gt = gt .. "</table>"
        return pandoc.RawBlock('html', gt)
      else
        -- Native Pandoc Table (handles escape/columns automatically for LaTeX/PDF)
        local rows = {}
        for _, key in ipairs(sortedKeys) do
          local def = globalGlossaryDefinitions[key]
          table.insert(rows, {
            { pandoc.Plain{pandoc.SmallCaps{pandoc.Str(key)}} },
            { pandoc.Plain{pandoc.Str(def)} }
          })
        end

        local header = {
          { pandoc.Plain{pandoc.Strong{pandoc.Str("Término")}} },
          { pandoc.Plain{pandoc.Strong{pandoc.Str("Definición")}} }
        }

        local st = pandoc.SimpleTable(
          {}, -- caption
          {pandoc.AlignLeft, pandoc.AlignLeft},
          {0.25, 0.75}, -- Widths
          header,
          rows
        )
        return pandoc.utils.from_simple_table(st)
      end
    end

    -- ── Inline term mode ───────────────────────────────────────────────────
    local display = ""
    if args[1] then
      display = pandoc.utils.stringify(args[1])
    end
    if kwExists(kwargs, "display") then
      display = pandoc.utils.stringify(kwargs.display)
    end

    local term = string.lower(display)
    local def = globalGlossaryDefinitions[term] or ""

    -- HTML: interactive tooltip button
    if quarto.doc.isFormat("html:js") then
      addHTMLDeps()
      local popup = options.popup
      local glosstext
      if popup == "hover" then
        glosstext = "<button class='glossary' title='" .. def .. "'>" .. display .. "</button>"
      elseif popup == "click" then
        glosstext = "<button class='glossary'><span class='def'>" .. def .. "</span>" .. display .. "</button>"
      else
        glosstext = "<button class='glossary'>" .. display .. "</button>"
      end
      return pandoc.RawInline("html", glosstext)

    -- PDF/LaTeX: small caps + footnote on first occurrence
    -- \texorpdfstring{body-text}{toc-text} ensures \footnote is safe
    -- in section headings (LaTeX uses toc-text for TOC/bookmarks)
    elseif quarto.doc.isFormat("latex") or quarto.doc.isFormat("pdf") then
      local scterm = "\\textsc{" .. escapeLaTeX(display) .. "}"
      if not globalTermsSeen[term] and def ~= "" then
        globalTermsSeen[term] = true
        local escaped_def = escapeLaTeX(def)
        local with_fn = scterm .. "\\footnote{" .. escaped_def .. "}"
        -- texorpdfstring: 1st arg = body (with footnote), 2nd = TOC bookmark (plain)
        return pandoc.RawInline("latex", "\\texorpdfstring{" .. with_fn .. "}{" .. scterm .. "}")
      else
        return pandoc.RawInline("latex", scterm)
      end

    else
      return pandoc.Str(display)
    end
  end
}
