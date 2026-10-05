#!/usr/bin/env python3
"""
Launcher automático do Projeto de Análise de Redes - Rock Alternativo (CEFET-MG Divinópolis).
Este script:
 1. Atualiza e exporta o bundle de dados JSON.
 2. Inicia o servidor HTTP local na porta 8000.
 3. Abre automaticamente a aplicação web no navegador por padrão.
"""
import sys
import os
import time
import socket
import urllib.request
import subprocess
import webbrowser

def check_port_in_use(port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def main():
    print("=" * 70)
    print("🎸  CEFET-MG Campus V (Divinópolis) - Análise de Redes de Rock Alternativo")
    print("    Alunos: Pedro H. S. C. | Orientador: Prof. Michel Pires da Silva")
    print("=" * 70)

    # 1. Exportar / Atualizar Bundle
    print("\n[1/3] 📦 Atualizando bundle de dados do grafo...")
    try:
        from src.exporters.export_json import generate_web_bundle
        generate_web_bundle('data/rock_collaborations_multi_genre.json', 'web/data/graph_bundle.json')
        print("  ✅ Bundle exportado com sucesso para 'web/data/graph_bundle.json'")
    except Exception as e:
        print(f"  ⚠️ Aviso ao exportar bundle: {e}")

    # 2. Verificar/Iniciar Servidor Web
    port = 8000
    server_url = f"http://localhost:{port}"
    server_process = None

    print(f"\n[2/3] 🌐 Verificando servidor web na porta {port}...")
    if check_port_in_use(port):
        print(f"  ✅ Servidor já está em execução em {server_url}")
    else:
        print(f"  🚀 Iniciando novo servidor HTTP na porta {port}...")
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
        server_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port)],
            cwd=web_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
        if check_port_in_use(port):
            print(f"  ✅ Servidor HTTP iniciado com sucesso em {server_url}")
        else:
            print("  ❌ Falha ao iniciar servidor HTTP.")

    # 3. Abrir Navegador
    print(f"\n[3/3] 🖥️  Abrindo Dashboard Web no navegador ({server_url})...")
    try:
        webbrowser.open(server_url)
        print("  ✅ Navegador aberto com sucesso!")
    except Exception as e:
        print(f"  ⚠️ Abra manualmente a URL no navegador: {server_url}")

    print("\n" + "=" * 70)
    print(f"✨ APLICAÇÃO PRONTA PARA USO!")
    print(f"📍 Acesse no seu navegador: {server_url}")
    print("   Pressione Ctrl+C para encerrar o terminal quando desejar.")
    print("=" * 70 + "\n")

    if server_process:
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Encerrando servidor HTTP...")
            server_process.terminate()
            print("👋 Até logo!")

if __name__ == "__main__":
    main()
