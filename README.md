# AI_RECORDER
Repositório para projeto jetson 
## Atualmente funcionam: 
* ai_recorder.py (grava e detecta pessoas e escreve para json, otimizado com periodo para ativar e desativar IA conferindo mais quadros de gravação)
* flask_server.py (faz upload de videos enviados via post)
* send_videos_light.py (envia apenas videos de ai_recorder, sem edição como 15 segundos antes e 45 depois)
## TODO:
* send_trimed_videos.py
* trimed_videos.py
