/**
 * Análise Topológica de Redes (Rock Alternativo) - App Controller (Vis.js Interactive Network)
 */

let network = null;
let rawBundleData = null;
let currentNodesDataset = null;
let currentEdgesDataset = null;

const COMMUNITY_COLORS = [
  '#58a6ff', '#bc8cff', '#3fb950', '#d29922', '#f85149',
  '#2f81f7', '#a5d6ff', '#7ee787', '#f2cc60', '#ff7b72',
  '#e36049', '#8957e5', '#38d9a9', '#f76707'
];

const GENRE_COLORS = {
  'Indie Rock': '#58a6ff',
  'Garage Rock Revival': '#bc8cff',
  'Indie Folk / Baroque': '#f76707',
  'Neo-Psychedelia': '#38d9a9',
  'Post-Rock': '#3fb950',
  'Math Rock / Emo': '#d29922',
  'Dance-Punk': '#f85149',
  'Alternative Rock': '#2f81f7',
  'Grunge': '#a5d6ff',
  'Post-Punk': '#7ee787',
  'Shoegaze': '#f2cc60',
  'Britpop': '#ff7b72',
  'Industrial': '#e36049',
  'New Wave': '#00d2d3',
  'Hardcore Punk': '#ff6b6b',
  'Noise Rock': '#ff9ff3',
  'College Rock': '#54a0ff'
};

const EDGE_COLORS = {
  'member': '#bc8cff',
  'producer': '#d29922',
  'guest': '#3fb950',
  'writer': '#58a6ff',
  'collaboration': '#58a6ff'
};

document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

async function initApp() {
  try {
    const res = await fetch('data/graph_bundle.json');
    rawBundleData = await res.json();

    setupEventListeners();
    setupExportFeatures();
    populateSearchAutofill();
    renderGraph();
    updateMetricsUI();
  } catch (err) {
    console.error("Erro ao carregar os dados do grafo:", err);
  }
}

function setupEventListeners() {
  document.getElementById('selectGenre').addEventListener('change', renderGraph);
  document.getElementById('selectBackbone').addEventListener('change', renderGraph);
  document.getElementById('selectColorBy').addEventListener('change', renderGraph);
  document.getElementById('chkShowEdgeLabels').addEventListener('change', renderGraph);
  document.getElementById('chkSimplifyTerminals').addEventListener('change', renderGraph);

  const rangeAlpha = document.getElementById('rangeAlpha');
  rangeAlpha.addEventListener('input', (e) => {
    document.getElementById('alphaValue').textContent = parseFloat(e.target.value).toFixed(2);
  });
  rangeAlpha.addEventListener('change', renderGraph);

  const rangeKmin = document.getElementById('rangeKmin');
  rangeKmin.addEventListener('input', (e) => {
    document.getElementById('kminValue').textContent = e.target.value;
  });
  rangeKmin.addEventListener('change', renderGraph);

  document.getElementById('btnResetView').addEventListener('click', () => {
    if (network) network.fit();
  });

  document.getElementById('nodeSearch').addEventListener('change', (e) => {
    const val = e.target.value.toLowerCase().trim();
    if (!val || !rawBundleData) return;

    const matchedNode = rawBundleData.nodes.find(n => n.label.toLowerCase() === val || n.id.toLowerCase() === val);
    if (matchedNode && network) {
      network.selectNodes([matchedNode.id]);
      network.focus(matchedNode.id, { scale: 1.2, animation: true });
      showNodeInspector(matchedNode.id);
    }
  });
}

function populateSearchAutofill() {
  const datalist = document.getElementById('artistList');
  if (!datalist || !rawBundleData) return;

  datalist.innerHTML = '';
  rawBundleData.nodes.forEach(n => {
    const opt = document.createElement('option');
    opt.value = n.label;
    datalist.appendChild(opt);
  });
}

function filterData() {
  const selectedGenre = document.getElementById('selectGenre').value;
  const backboneMode = document.getElementById('selectBackbone').value;
  const kMin = parseInt(document.getElementById('rangeKmin').value, 10);
  const alpha = parseFloat(document.getElementById('rangeAlpha').value);

  let filteredNodes = [...rawBundleData.nodes];
  let filteredEdges = [...rawBundleData.edges];

  if (selectedGenre !== 'All') {
    const targetIds = new Set(filteredNodes.filter(n => n.genre === selectedGenre).map(n => n.id));
    const neighborIds = new Set();
    filteredEdges.forEach(e => {
      if (targetIds.has(e.source)) neighborIds.add(e.target);
      if (targetIds.has(e.target)) neighborIds.add(e.source);
    });
    const validIds = new Set([...targetIds, ...neighborIds]);

    filteredNodes = filteredNodes.filter(n => validIds.has(n.id));
    filteredEdges = filteredEdges.filter(e => validIds.has(e.source) && validIds.has(e.target));
  }

  filteredEdges = filteredEdges.map(e => {
    const wRawNorm = e.weight_raw / 15.0;
    const qNorm = e.critic_score / 100.0;
    const wHybrid = alpha * wRawNorm + (1.0 - alpha) * qNorm;
    return { ...e, weight: Math.max(0.1, wHybrid) };
  });

  if (kMin > 1) {
    const degMap = {};
    filteredEdges.forEach(e => {
      degMap[e.source] = (degMap[e.source] || 0) + 1;
      degMap[e.target] = (degMap[e.target] || 0) + 1;
    });

    const validKminIds = new Set(filteredNodes.filter(n => (degMap[n.id] || 0) >= kMin).map(n => n.id));
    filteredNodes = filteredNodes.filter(n => validKminIds.has(n.id));
    filteredEdges = filteredEdges.filter(e => validKminIds.has(e.source) && validKminIds.has(e.target));
  }

  if (backboneMode === 'mst') {
    filteredEdges = filteredEdges.sort((a, b) => b.weight - a.weight).slice(0, Math.max(1, filteredNodes.length - 1));
  } else if (backboneMode === 'bridges') {
    filteredEdges = filteredEdges.filter(e => e.weight > 0.5);
  }

  return { nodes: filteredNodes, edges: filteredEdges };
}

function renderGraph() {
  const container = document.getElementById('networkCanvas');
  const { nodes, edges } = filterData();
  const colorBy = document.getElementById('selectColorBy').value;
  const showEdgeLabels = document.getElementById('chkShowEdgeLabels').checked;
  const simplifyTerminals = document.getElementById('chkSimplifyTerminals').checked;

  const localDegMap = {};
  edges.forEach(e => {
    localDegMap[e.source] = (localDegMap[e.source] || 0) + 1;
    localDegMap[e.target] = (localDegMap[e.target] || 0) + 1;
  });

  const visNodes = nodes.map(n => {
    let color = '#58a6ff';
    if (colorBy === 'community') {
      color = COMMUNITY_COLORS[n.community % COMMUNITY_COLORS.length];
    } else if (colorBy === 'genre') {
      color = GENRE_COLORS[n.genre] || '#8b949e';
    } else if (colorBy === 'type') {
      color = n.type === 'band' ? '#bc8cff' : (n.type_role === 'producer' ? '#d29922' : '#58a6ff');
    }

    const localDegree = localDegMap[n.id] || n.degree || 0;
    const isTerminal = localDegree <= 1;

    const size = (simplifyTerminals && isTerminal) ? 6 : Math.max(12, Math.min(36, 12 + localDegree * 2));
    const labelText = (simplifyTerminals && isTerminal) ? "" : n.label;
    const opacity = (simplifyTerminals && isTerminal) ? 0.6 : 1.0;

    return {
      id: n.id,
      label: labelText,
      title: `${n.label} (${n.genre}) - Grau ${localDegree}`,
      shape: n.type === 'band' ? 'diamond' : (n.type_role === 'producer' ? 'square' : 'dot'),
      size: size,
      color: {
        background: color,
        border: '#ffffff',
        highlight: { background: '#ffffff', border: color }
      },
      opacity: opacity,
      font: { color: '#f0f6fc', face: 'Inter', size: 12 }
    };
  });

  const visEdges = edges.map((e, idx) => {
    const edgeColor = EDGE_COLORS[e.relation_type] || '#58a6ff';
    const edgeId = `edge_${e.source}_${e.target}`;

    return {
      id: edgeId,
      from: e.source,
      to: e.target,
      label: showEdgeLabels ? (e.relation_label || e.relation_type) : '',
      font: { color: edgeColor, face: 'Inter', size: 10, strokeWidth: 2, strokeColor: '#090d16', align: 'horizontal' },
      width: Math.max(1.5, Math.min(6, e.weight * 4)),
      color: { color: edgeColor, opacity: 0.65, highlight: '#ffffff' },
      smooth: { type: 'continuous' },
      rawEdgeData: e
    };
  });

  currentNodesDataset = new vis.DataSet(visNodes);
  currentEdgesDataset = new vis.DataSet(visEdges);

  const data = { nodes: currentNodesDataset, edges: currentEdgesDataset };
  const options = {
    physics: {
      barnesHut: { gravitationalConstant: -4500, centralGravity: 0.3, springLength: 110 },
      stabilization: { iterations: 150 }
    },
    interaction: { hover: true, tooltipDelay: 150, selectConnectedEdges: true }
  };

  if (network) network.destroy();
  network = new vis.Network(container, data, options);

  network.on('click', (params) => {
    if (params.nodes.length > 0) {
      showNodeInspector(params.nodes[0]);
    } else if (params.edges.length > 0) {
      showEdgeInspector(params.edges[0]);
    }
  });

  updateMetricsUI(nodes.length, edges.length);
}

function updateMetricsUI(nCount, mCount) {
  if (!rawBundleData) return;
  const gm = rawBundleData.global_metrics;

  document.getElementById('statNodes').textContent = nCount !== undefined ? nCount : gm.num_nodes;
  document.getElementById('statEdges').textContent = mCount !== undefined ? mCount : gm.num_edges;
  document.getElementById('statDensity').textContent = gm.density;
  document.getElementById('statClustering').textContent = gm.avg_clustering;
  document.getElementById('statPathLength').textContent = gm.avg_shortest_path;
  document.getElementById('statModularity').textContent = gm.modularity;

  const swIndex = gm.small_world_index !== undefined ? gm.small_world_index : 0.0;
  const isSW = swIndex > 1.0;
  const swBadge = document.getElementById('statSmallWorld');
  swBadge.parentNode.style.background = isSW ? 'rgba(63, 185, 80, 0.1)' : 'rgba(210, 153, 34, 0.1)';
  swBadge.parentNode.style.borderColor = isSW ? 'rgba(63, 185, 80, 0.2)' : 'rgba(210, 153, 34, 0.2)';
  swBadge.parentNode.style.color = isSW ? 'var(--accent-emerald)' : 'var(--accent-amber)';
  swBadge.innerHTML = `S = ${swIndex} ${isSW ? '✅ (Mundo Pequeno Válido no LCC)' : '⚠️ (Rede Modular)'}`;

  const pl = rawBundleData.power_law;
  document.getElementById('statPowerLaw').innerHTML = `γ = ${pl.gamma} (R² = ${pl.r_squared}) ${pl.is_scale_free ? '✅ Scale-Free Válido' : '⚠️ Distribuição Normal'}`;
}

function showEdgeInspector(edgeId) {
  const visEdge = currentEdgesDataset.get(edgeId);
  if (!visEdge || !visEdge.rawEdgeData) return;

  const e = visEdge.rawEdgeData;
  const srcNode = rawBundleData.nodes.find(n => n.id === e.source);
  const tgtNode = rawBundleData.nodes.find(n => n.id === e.target);

  const srcName = srcNode ? srcNode.label : e.source;
  const tgtName = tgtNode ? tgtNode.label : e.target;

  const sidebar = document.getElementById('inspectorContent');
  const worksText = e.works && e.works.length > 0 ? e.works.join(', ') : 'Parceria em faixas/álbuns';

  sidebar.innerHTML = `
    <div class="inspector-header">
      <h3>🔗 Relação Exata entre Artistas</h3>
      <span class="sub-badge" style="background: rgba(188, 140, 255, 0.2); color: var(--accent-purple);">${e.relation_label.toUpperCase()}</span>
    </div>

    <div style="background: rgba(255,255,255,0.04); border-radius: 8px; padding: 12px; border: 1px solid var(--border-color); margin-bottom: 14px;">
      <div style="font-size: 14px; font-weight: 700; color: var(--accent-cyan);">${srcName}  🤝  ${tgtName}</div>
      <div style="margin-top: 8px; font-size: 13px; color: var(--accent-emerald); font-weight: 600;">
        📌 Descrição da Relação:
      </div>
      <div style="font-size: 12px; color: var(--text-bright); margin-top: 2px;">
        ${e.relation_desc}
      </div>
    </div>

    <div class="stat-row"><span>Tipo da Relação:</span> <strong>${e.relation_type}</strong></div>
    <div class="stat-row"><span>Nota da Crítica:</span> <strong>${e.critic_score} / 100</strong></div>
    <div class="stat-row"><span>Contagem de Trabalhos:</span> <strong>${e.weight_raw} colaboração(ões)</strong></div>
    <div class="stat-row"><span>Peso Híbrido Ajustado:</span> <strong>${e.weight.toFixed(3)}</strong></div>

    <h4 style="margin-top: 16px; font-size: 13px; font-family: 'Outfit'; color: var(--text-bright);">Obras Realizadas em Conjunto:</h4>
    <div class="collab-item" style="margin-top: 6px;">
      <div class="collab-meta" style="font-size: 12px; color: var(--text-main);">
        💿 <em>${worksText}</em>
      </div>
    </div>
  `;
}

function showNodeInspector(nodeId) {
  const node = rawBundleData.nodes.find(n => n.id === nodeId);
  if (!node) return;

  const sidebar = document.getElementById('inspectorContent');
  const collabs = rawBundleData.edges.filter(e => e.source === nodeId || e.target === nodeId);

  let collabsHTML = collabs.map(e => {
    const targetId = e.source === nodeId ? e.target : e.source;
    const targetNode = rawBundleData.nodes.find(n => n.id === targetId);
    const targetName = targetNode ? targetNode.label : targetId;
    const worksText = e.works && e.works.length > 0 ? e.works.join(', ') : 'Parceria';

    return `
      <div class="collab-item">
        <div class="target-name">
          <span>🤝 ${targetName}</span>
          <span class="rel-tag">${e.relation_label || e.relation_type}</span>
        </div>
        <div class="rel-desc">📌 ${e.relation_desc}</div>
        <div class="collab-meta">
          <span>Obras: <em>${worksText}</em> | Nota Crítica: <strong>${e.critic_score}/100</strong></span>
        </div>
      </div>
    `;
  }).join('');

  sidebar.innerHTML = `
    <div class="inspector-header">
      <h3>${node.label}</h3>
      <span class="sub-badge">${node.genre} | ${node.type === 'band' ? 'Banda' : (node.type_role === 'producer' ? 'Produtor Musical' : 'Artista')}</span>
    </div>

    <div class="stat-row"><span>Grau (Degree k):</span> <strong>${node.degree}</strong></div>
    <div class="stat-row"><span>Força (Strength s):</span> <strong>${node.strength}</strong></div>
    <div class="stat-row"><span>Intermediação (Betweenness):</span> <strong>${node.betweenness}</strong></div>
    <div class="stat-row"><span>Proximidade (Closeness):</span> <strong>${node.closeness}</strong></div>
    <div class="stat-row"><span>PageRank:</span> <strong>${node.pagerank}</strong></div>
    <div class="stat-row"><span>Comunidade (Louvain):</span> <strong>Comunidade #${node.community}</strong></div>

    <h4 style="margin-top: 16px; font-size: 13px; font-family: 'Outfit'; color: var(--text-bright);">Colaborações Exatas (${collabs.length}):</h4>
    <div class="collab-list">
      ${collabsHTML || '<p style="color: var(--text-muted); font-size: 12px;">Sem colaborações ativas.</p>'}
    </div>
  `;
}

/* ==========================================================================
   MÓDULO DE EXPORTAÇÃO / PRINT DO GRAFO EM ALTA RESOLUÇÃO (4K)
   Suporte a Fundo Branco (Artigo/LaTeX) e Fundo Preto (Tema Escuro)
   ========================================================================== */

function setupExportFeatures() {
  // Botões de captura rápida na barra do canvas
  const btnWhite = document.getElementById('btnQuickExportWhite');
  if (btnWhite) {
    btnWhite.addEventListener('click', () => {
      exportGraphSnapshot({
        theme: 'white',
        scope: 'full',
        resolution: '3840x2160',
        includeLegend: true,
        showLabels: true
      });
    });
  }

  const btnBlack = document.getElementById('btnQuickExportBlack');
  if (btnBlack) {
    btnBlack.addEventListener('click', () => {
      exportGraphSnapshot({
        theme: 'black',
        scope: 'full',
        resolution: '3840x2160',
        includeLegend: true,
        showLabels: true
      });
    });
  }

  // Abertura do Modal de Exportação
  const btnHeader = document.getElementById('btnHeaderExport');
  if (btnHeader) btnHeader.addEventListener('click', openExportModal);

  const btnOptions = document.getElementById('btnQuickExportOptions');
  if (btnOptions) btnOptions.addEventListener('click', openExportModal);

  // Fechamento do Modal
  const btnClose = document.getElementById('btnCloseModal');
  if (btnClose) btnClose.addEventListener('click', closeExportModal);

  const btnCancel = document.getElementById('btnCancelModal');
  if (btnCancel) btnCancel.addEventListener('click', closeExportModal);

  const modal = document.getElementById('exportModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target.id === 'exportModal') closeExportModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeExportModal();
  });

  // Seletor visual de temas dentro do modal (Cards Branco vs Preto)
  const themeOptWhite = document.getElementById('themeOptWhite');
  const themeOptBlack = document.getElementById('themeOptBlack');
  if (themeOptWhite && themeOptBlack) {
    themeOptWhite.addEventListener('click', () => {
      themeOptWhite.classList.add('selected');
      themeOptBlack.classList.remove('selected');
      themeOptWhite.querySelector('input').checked = true;
    });

    themeOptBlack.addEventListener('click', () => {
      themeOptBlack.classList.add('selected');
      themeOptWhite.classList.remove('selected');
      themeOptBlack.querySelector('input').checked = true;
    });
  }

  // Botão de download do modal
  const btnConfirm = document.getElementById('btnConfirmExport');
  if (btnConfirm) {
    btnConfirm.addEventListener('click', () => {
      const selectedTheme = document.querySelector('input[name="exportTheme"]:checked')?.value || 'white';
      const scope = document.getElementById('exportScope')?.value || 'full';
      const resolution = document.getElementById('exportResolution')?.value || '3840x2160';
      const includeLegend = document.getElementById('chkExportLegend')?.checked ?? true;
      const showLabels = document.getElementById('chkExportLabels')?.checked ?? true;

      closeExportModal();

      exportGraphSnapshot({
        theme: selectedTheme,
        scope: scope,
        resolution: resolution,
        includeLegend: includeLegend,
        showLabels: showLabels
      });
    });
  }
}

function openExportModal() {
  const modal = document.getElementById('exportModal');
  if (modal) modal.style.display = 'flex';
}

function closeExportModal() {
  const modal = document.getElementById('exportModal');
  if (modal) modal.style.display = 'none';
}

/**
 * Função Principal de Exportação do Grafo em Alta Resolução
 */
function exportGraphSnapshot(opts) {
  const theme = opts.theme || 'white';
  const scope = opts.scope || 'full';
  const resolutionStr = opts.resolution || '3840x2160';
  const includeLegend = opts.includeLegend !== undefined ? opts.includeLegend : true;
  const showLabels = opts.showLabels !== undefined ? opts.showLabels : true;

  const [targetWidth, targetHeight] = resolutionStr.split('x').map(Number);
  const isWhite = theme === 'white';

  showExportToast('⏳ Gerando print em alta definição (4K)... Aguarde um instante.', true);

  // Se o escopo for viewport (print da tela atual exata)
  if (scope === 'viewport') {
    exportCurrentViewport(isWhite, includeLegend);
    return;
  }

  // Para 'full' ou 'lcc', geramos via offscreen Vis.js para máxima nitidez (4K/8K)
  // Obter dados filtrados ativos
  const { nodes, edges } = filterData();
  const colorBy = document.getElementById('selectColorBy')?.value || 'genre';
  const simplifyTerminals = document.getElementById('chkSimplifyTerminals')?.checked ?? false;
  const showEdgeLabels = document.getElementById('chkShowEdgeLabels')?.checked ?? false;

  // Grau local para escalonamento
  const localDegMap = {};
  edges.forEach(e => {
    localDegMap[e.source] = (localDegMap[e.source] || 0) + 1;
    localDegMap[e.target] = (localDegMap[e.target] || 0) + 1;
  });

  // Filtrar nós se for foco no LCC
  let targetNodes = nodes;
  let targetEdges = edges;
  if (scope === 'lcc') {
    // Nós conectados (grau >= 1 no filtro ativo)
    const activeIds = new Set(nodes.filter(n => (localDegMap[n.id] || 0) >= 1).map(n => n.id));
    targetNodes = nodes.filter(n => activeIds.has(n.id));
    targetEdges = edges.filter(e => activeIds.has(e.source) && activeIds.has(e.target));
  }

  // Coordenadas calculadas da simulação ativa no canvas principal
  const currentPositions = network ? network.getPositions() : {};

  // Fator de escala baseado na resolução (ex: 3840 = 2x escala de 1920)
  const scaleMultiplier = Math.max(1.0, targetWidth / 1920.0);

  // Preparar os nós estilizados para o tema escolhido
  const exportVisNodes = targetNodes.map(n => {
    let color = '#58a6ff';
    if (colorBy === 'community') {
      color = COMMUNITY_COLORS[n.community % COMMUNITY_COLORS.length];
    } else if (colorBy === 'genre') {
      color = GENRE_COLORS[n.genre] || '#8b949e';
    } else if (colorBy === 'type') {
      color = n.type === 'band' ? '#bc8cff' : (n.type_role === 'producer' ? '#d29922' : '#58a6ff');
    }

    const localDegree = localDegMap[n.id] || n.degree || 0;
    const isTerminal = localDegree <= 1;

    // Tamanho proporcional do nó
    const baseSize = (simplifyTerminals && isTerminal)
      ? 7
      : Math.max(14, Math.min(42, 14 + localDegree * 2.2));
    const finalSize = Math.round(baseSize * scaleMultiplier);

    // Rótulo
    let labelText = n.label;
    if (!showLabels) {
      labelText = '';
    } else if (simplifyTerminals && isTerminal) {
      labelText = '';
    }

    // Posição fixa preservando o layout da simulação
    const pos = currentPositions[n.id] || { x: (Math.random() - 0.5) * 2000, y: (Math.random() - 0.5) * 2000 };

    return {
      id: n.id,
      label: labelText,
      shape: n.type === 'band' ? 'diamond' : (n.type_role === 'producer' ? 'square' : 'dot'),
      size: finalSize,
      x: pos.x,
      y: pos.y,
      fixed: true,
      color: {
        background: color,
        border: isWhite ? '#1e293b' : '#ffffff',
        highlight: { background: '#ffffff', border: color }
      },
      borderWidth: Math.max(1.5, Math.round(1.8 * scaleMultiplier)),
      font: {
        color: isWhite ? '#0f172a' : '#f8fafc',
        face: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        size: Math.round(13 * scaleMultiplier),
        strokeWidth: Math.round(3.5 * scaleMultiplier),
        strokeColor: isWhite ? '#ffffff' : '#090d16',
        vadjust: Math.round(2 * scaleMultiplier)
      },
      opacity: (simplifyTerminals && isTerminal) ? 0.75 : 1.0
    };
  });

  // Preparar as arestas estilizadas para o tema escolhido
  const exportVisEdges = targetEdges.map(e => {
    const edgeColor = EDGE_COLORS[e.relation_type] || '#58a6ff';
    return {
      id: `export_edge_${e.source}_${e.target}`,
      from: e.source,
      to: e.target,
      label: showEdgeLabels ? (e.relation_label || e.relation_type) : '',
      font: {
        color: isWhite ? '#1e293b' : edgeColor,
        face: 'Inter, sans-serif',
        size: Math.round(10 * scaleMultiplier),
        strokeWidth: Math.round(2.5 * scaleMultiplier),
        strokeColor: isWhite ? '#ffffff' : '#090d16',
        align: 'horizontal'
      },
      width: Math.max(1.8 * scaleMultiplier, Math.min(7 * scaleMultiplier, (e.weight || 0.5) * 3.8 * scaleMultiplier)),
      color: {
        color: edgeColor,
        opacity: isWhite ? 0.75 : 0.65
      },
      smooth: { type: 'continuous' }
    };
  });

  // Criar container invisível para renderização off-screen
  const tempContainer = document.createElement('div');
  tempContainer.id = 'tempOffscreenNetwork';
  tempContainer.style.position = 'fixed';
  tempContainer.style.left = '-35000px';
  tempContainer.style.top = '-35000px';
  tempContainer.style.width = `${targetWidth}px`;
  tempContainer.style.height = `${targetHeight}px`;
  tempContainer.style.zIndex = '-9999';
  document.body.appendChild(tempContainer);

  const exportData = {
    nodes: new vis.DataSet(exportVisNodes),
    edges: new vis.DataSet(exportVisEdges)
  };

  const exportOptions = {
    physics: { enabled: false }, // Layout estático baseado nas posições calculadas
    interaction: { dragNodes: false, dragView: false, zoomView: false }
  };

  const tempNetwork = new vis.Network(tempContainer, exportData, exportOptions);

  // Enquadrar perfeitamente todos os nós, garantindo que as extremidades não sejam cortadas
  tempNetwork.fit({ animation: false });

  // Aguarda rasterização gráfica do canvas
  setTimeout(() => {
    try {
      const rawCanvas = tempContainer.querySelector('canvas');
      if (!rawCanvas) throw new Error("Canvas de renderização não encontrado");

      // Canvas final com fundo sólido e legenda
      const finalCanvas = document.createElement('canvas');
      finalCanvas.width = targetWidth;
      finalCanvas.height = targetHeight;
      const ctx = finalCanvas.getContext('2d');

      // 1. Pinta o fundo escolhido
      ctx.fillStyle = isWhite ? '#ffffff' : '#090d16';
      ctx.fillRect(0, 0, targetWidth, targetHeight);

      // 2. Desenha o grafo em alta definição
      ctx.drawImage(rawCanvas, 0, 0, targetWidth, targetHeight);

      // 3. Rodapé acadêmico / legenda se solicitado
      if (includeLegend) {
        drawAcademicLegend(ctx, targetWidth, targetHeight, theme);
      }

      // 4. Download do arquivo PNG
      const themeLabel = isWhite ? 'fundo_branco' : 'fundo_preto';
      const scopeLabel = scope === 'full' ? 'completo' : scope;
      const filename = `grafo_${scopeLabel}_rock_alternativo_${themeLabel}_${targetWidth}x${targetHeight}.png`;

      const dataUrl = finalCanvas.toDataURL('image/png');
      triggerDownload(dataUrl, filename);

      showExportToast(`✅ Print ${isWhite ? 'Fundo Branco' : 'Fundo Preto'} (${targetWidth}x${targetHeight}) baixado com sucesso!`, false);
    } catch (err) {
      console.error("Erro ao gerar print do grafo:", err);
      showExportToast('❌ Erro ao exportar o grafo. Tente novamente.', false);
    } finally {
      tempNetwork.destroy();
      tempContainer.remove();
    }
  }, 220);
}

/**
 * Captura direta da visão atual (viewport)
 */
function exportCurrentViewport(isWhite, includeLegend) {
  const screenCanvas = document.querySelector('#networkCanvas canvas');
  if (!screenCanvas) {
    showExportToast('❌ Canvas da rede não disponível.', false);
    return;
  }

  const width = screenCanvas.width;
  const height = screenCanvas.height;

  // Se fundo branco na visão atual, ajustamos temporariamente o dataset para contraste
  if (isWhite && currentNodesDataset) {
    const originalNodes = currentNodesDataset.get();
    const whiteUpdates = originalNodes.map(n => ({
      id: n.id,
      font: { color: '#0f172a', strokeColor: '#ffffff', strokeWidth: 3 },
      color: { ...n.color, border: '#1e293b' }
    }));

    currentNodesDataset.update(whiteUpdates);
    network.redraw();

    setTimeout(() => {
      saveViewportCanvas(screenCanvas, width, height, true, includeLegend);
      // Restaura nós
      currentNodesDataset.update(originalNodes);
      network.redraw();
    }, 100);
  } else {
    saveViewportCanvas(screenCanvas, width, height, false, includeLegend);
  }
}

function saveViewportCanvas(screenCanvas, width, height, isWhite, includeLegend) {
  const finalCanvas = document.createElement('canvas');
  finalCanvas.width = width;
  finalCanvas.height = height;
  const ctx = finalCanvas.getContext('2d');

  ctx.fillStyle = isWhite ? '#ffffff' : '#090d16';
  ctx.fillRect(0, 0, width, height);
  ctx.drawImage(screenCanvas, 0, 0);

  if (includeLegend) {
    drawAcademicLegend(ctx, width, height, isWhite ? 'white' : 'black');
  }

  const filename = `grafo_visao_atual_rock_alternativo_${isWhite ? 'fundo_branco' : 'fundo_preto'}.png`;
  const dataUrl = finalCanvas.toDataURL('image/png');
  triggerDownload(dataUrl, filename);

  showExportToast(`✅ Print da visão atual (${isWhite ? 'Fundo Branco' : 'Fundo Preto'}) baixado com sucesso!`, false);
}

/**
 * Desenha Banner de Legenda Científica e Métricas Topológicas no Rodapé
 */
function drawAcademicLegend(ctx, width, height, theme) {
  const isWhite = theme === 'white';
  const bannerHeight = Math.max(72, Math.round(height * 0.058));
  const y = height - bannerHeight;

  ctx.save();

  // Fundo com leve transparência e blur estético
  ctx.fillStyle = isWhite ? 'rgba(248, 250, 252, 0.96)' : 'rgba(13, 17, 23, 0.94)';
  ctx.fillRect(0, y, width, bannerHeight);

  // Linha superior divisória
  ctx.strokeStyle = isWhite ? '#cbd5e1' : 'rgba(88, 166, 255, 0.25)';
  ctx.lineWidth = Math.max(1, Math.round(width * 0.0007));
  ctx.beginPath();
  ctx.moveTo(0, y);
  ctx.lineTo(width, y);
  ctx.stroke();

  // Cores de texto
  const primaryText = isWhite ? '#0f172a' : '#f0f6fc';
  const secondaryText = isWhite ? '#475569' : '#8b949e';
  const accentColor = isWhite ? '#0284c7' : '#58a6ff';

  const titleFontSize = Math.max(13, Math.round(width * 0.0068));
  const subFontSize = Math.max(10, Math.round(width * 0.0052));

  // Título à esquerda
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  ctx.font = `bold ${titleFontSize}px 'Outfit', Inter, sans-serif`;
  ctx.fillStyle = primaryText;
  ctx.fillText('Supergrafo de Colaborações — Rock dos Anos 80 e 90 & Cenas Correlatas', 28, y + bannerHeight * 0.2);

  // Métricas científicas no subtítulo
  ctx.font = `${subFontSize}px 'Inter', sans-serif`;
  ctx.fillStyle = secondaryText;

  let metricsStr = 'Teoria dos Grafos & Ciência das Redes Complexas';
  if (rawBundleData && rawBundleData.global_metrics) {
    const gm = rawBundleData.global_metrics;
    metricsStr = `N = ${gm.num_nodes} nós | M = ${gm.num_edges} colaborações | LCC = ${gm.num_lcc_nodes} nós (${((gm.num_lcc_nodes / gm.num_nodes) * 100).toFixed(1)}%) | Densidade = ${gm.density} | Modularidade Q = ${gm.modularity}`;
  }
  ctx.fillText(metricsStr, 28, y + bannerHeight * 0.58);

  // Legenda de formas e arestas à direita
  ctx.textAlign = 'right';
  ctx.font = `600 ${subFontSize}px 'Inter', sans-serif`;
  ctx.fillStyle = primaryText;
  const legendRight = width - 28;
  ctx.fillText('◆ Banda / Grupo    ■ Produtor Musical    ● Artista Solo    |    — Integrante   — Produção   — Colaboração', legendRight, y + bannerHeight * 0.38);

  ctx.restore();
}

/**
 * Disparo automático de download no navegador
 */
function triggerDownload(dataUrl, filename) {
  const link = document.createElement('a');
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Exibe notificação toast na tela
 */
function showExportToast(msg, isProcessing) {
  const toast = document.getElementById('exportToast');
  const icon = document.getElementById('exportToastIcon');
  const text = document.getElementById('exportToastMsg');
  if (!toast) return;

  icon.textContent = isProcessing ? '⏳' : (msg.includes('❌') ? '❌' : '✅');
  text.textContent = msg;
  toast.style.display = 'flex';

  if (!isProcessing) {
    setTimeout(() => {
      toast.style.display = 'none';
    }, 4500);
  }
}

