import re

def triage_report(report_path, output_path):
    with open(report_path, 'r') as f:
        lines = f.readlines()
    
    curated = "# Reporte Curado: Errores Sugeridos para Corrección\n\n"
    curated += "He filtrado el reporte original para eliminar el 'ruido' de formato (espacios múltiples, artefactos de Quarto) y centrarme en errores lingüísticos reales.\n\n"
    
    current_chapter = ""
    findings = []
    
    # Simple state machine to parse the report
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            current_chapter = line.strip()
            findings.append(f"\n{current_chapter}\n")
        
        if line.startswith("- **Hallazgo:**"):
            msg = line
            word_line = lines[i+1] if i+1 < len(lines) else ""
            context_line = lines[i+2] if i+2 < len(lines) else ""
            sugg_line = lines[i+3] if i+3 < len(lines) else ""
            
            # Filter logic
            is_noise = False
            if "múltiples espacios en blanco" in msg: is_noise = True
            if ".callout" in word_line or ".content" in word_line: is_noise = True
            if "_blank" in word_line: is_noise = True
            if "watch?v=" in context_line: is_noise = True
            if "Símbolo desparejado" in msg and "<" in word_line: is_noise = True
            
            # Keep if NOT noise
            if not is_noise:
                findings.append(f"{msg}{word_line}{context_line}{sugg_line}\n")
            
            i += 3 # Skip to next candidate
        i += 1
        
    with open(output_path, 'w') as out:
        out.writelines(findings)

if __name__ == "__main__":
    triage_report('artifacts/grammar_report.md', 'artifacts/curated_grammar_report.md')
