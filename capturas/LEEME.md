## Guía de capturas pendientes — ltq2

Esta carpeta contiene (o contendrá) los frames de video que funcionan como ilustraciones en los capítulos.

### Convención de archivos

```
cap01_c01_[youtuber]_[descripcion].png
cap02_c01_[youtuber]_[descripcion].png
cap03_c01_[youtuber]_[descripcion].png
```

### Workflow sugerido

1. Pausar el video en YouTube en el segundo indicado en el placeholder
2. Tomar captura de pantalla (o usar `yt-dlp --skip-download --write-thumbnail` para extraer el frame exacto)
3. Recortar solo el frame del video (sin la interfaz de YouTube)
4. Guardar con el nombre indicado en el placeholder
5. Completar la URL con el `?t=Xs` correcto en el QMD

### Capturas pendientes por capítulo

| ID | Capítulo | Youtuber sugerido | Descripción del frame | Archivo |
|---|---|---|---|---|
| CAP01-C01 | 01_intro | Lucas Castel o Julián Serrano | Setup de dormitorio típico del período 2013-2014: cámara al frente, estante con cosas de fondo, iluminación natural o lámpara de escritorio | `cap01_c01_setup_dormitorio.png` |
| CAP02-C01 | 02_mtya | Cualquiera que tenga escena de confesión / cercanía a cámara | Primer plano del youtuber mirando directamente a cámara, expresión de confianza o vulnerabilidad — ideal para ilustrar extimidad | `cap02_c01_extimidad_camara.png` |
| CAP03-C01 | 03_metod | Variedad: usar una imagen por youtuber o un collage 2×4 | Frame representativo de cada uno de los 8 youtubers en su setup habitual — para poner rostros a la tabla del corpus | `cap03_c01_corpus_collage.png` |
| CAP03-C02 | 03_metod | Lucas Castel (exterior) vs. Julián Serrano (dormitorio) | Contraste de escenarios: interior vs exterior, para ilustrar la variedad de escenarios codificados | `cap03_c02_escenarios_contraste.png` |
| CAP03-C03 | 03_metod | Cualquiera con backstage visible | Frame mostrando un elemento de backstage (goffmaniano): ropa informal, habitación "real", mascotas, familia entrando, etc. | `cap03_c03_backstage.png` |

---

### Nota sobre la versión web (HTML)

Los placeholders en los QMDs ya incluyen el bloque HTML-only con el link de YouTube:

```markdown
::: {.content-visible when-format="html"}
[▶ Ver este momento en YouTube](https://www.youtube.com/watch?v=VIDEO_ID&t=XXs){target="_blank"}
:::
```

Solo reemplazar `VIDEO_ID` y `XX` (segundos) cuando tengas el frame elegido.
