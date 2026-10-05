"""
Módulo para cálculo de peso híbrido ajustável entre Frequência Bruta e Impacto Crítico.
"""
import numpy as np


def compute_hybrid_weights(edges, alpha=0.5):
    """
    Calcula o peso híbrido para cada aresta em uma lista de arestas com atributos.

    Fórmula:
    W_hibrido(i, j) = alpha * W_bruto_norm(i, j) + (1 - alpha) * Q_critica_norm(i, j)

    Parâmetros:
    -----------
    edges : list[dict]
        Lista de dicionários de arestas contendo 'weight_count' e 'critic_score'.
    alpha : float (0.0 a 1.0)
        Fator de ponderação:
        alpha = 1.0 -> 100% Frequência Bruta (Topologia Pura)
        alpha = 0.5 -> Equilíbrio 50% Frequência / 50% Crítica
        alpha = 0.0 -> 100% Impacto Crítico (Qualidade/Aclamação)

    Retorna:
    --------
    list[dict]
        Lista de arestas atualizadas com a chave 'weight_hybrid' e pesos normalizados.
    """
    if not edges:
        return []

    # Extrair listas brutas
    raw_weights = np.array([e.get("weight_count", 1) for e in edges], dtype=float)
    critic_scores = np.array([e.get("critic_score", 50) for e in edges], dtype=float)

    # Normalizar W_bruto entre 0 e 1 (min-max)
    min_w, max_w = np.min(raw_weights), np.max(raw_weights)
    if max_w > min_w:
        w_norm = (raw_weights - min_w) / (max_w - min_w)
    else:
        w_norm = np.ones_like(raw_weights)

    # Normalizar Q_critica entre 0 e 1 (assumindo escala 0-100)
    q_norm = critic_scores / 100.0
    q_norm = np.clip(q_norm, 0.0, 1.0)

    # Garantir que alpha esteja no intervalo [0, 1]
    alpha_clamped = np.clip(alpha, 0.0, 1.0)

    # Calcular peso híbrido
    h_weights = alpha_clamped * w_norm + (1.0 - alpha_clamped) * q_norm

    # Reatribuir aos dicionários de arestas
    result_edges = []
    for idx, e in enumerate(edges):
        e_copy = dict(e)
        e_copy["weight_raw_norm"] = float(w_norm[idx])
        e_copy["critic_score_norm"] = float(q_norm[idx])
        e_copy["weight_hybrid"] = float(h_weights[idx])
        # Manter compatibilidade com peso padronizado
        e_copy["weight"] = float(h_weights[idx])
        result_edges.append(e_copy)

    return result_edges
