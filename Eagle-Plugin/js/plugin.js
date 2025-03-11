// ==================== 全局状态控制 ====================
let abortController = null;
let isTaggingActive = false;
let progress = {
  current: 0,
  total: 0,
  cancelled: false
};
let chunkSize = 32; // 默认分块大小
let maxChunkSize = 192; //
DEFAULT_LANGUAGE = 'zh_cn';

// ==================== UI 模板 ====================
const uiTemplate = () => `
  <div class="container">
    <header class="header">
      <img src="${eagle.plugin.manifest.logo}" class="logo" alt="AntLLM Logo">
      <h1>AntLLM 🐜 智能文件管理 </h1>
      <h1>v${eagle.plugin.manifest.version}</h1>
    </header>

    <div class="config-group">
      <div class="input-group">
        <label>分块大小：</label>
        <input 
          type="number" 
          id="chunkSize" 
          min="1" 
          max="${maxChunkSize}" 
          value="${chunkSize}"
          ${isTaggingActive ? 'disabled' : ''}
          onchange="updateChunkSize(this.value)"
        >
        <span class="hint">(1-${maxChunkSize})</span>
      </div>
    </div>

    <div class="control-group">
      <button class="btn primary" onclick="handleTagging(false)">
        <span class="icon">🏷️</span>智能打标
      </button>
      <button class="btn warning" onclick="confirmForceRefresh()">
        <span class="icon">🔄</span>强制刷新
      </button>
      <button class="btn danger" onclick="handleCancel()" ${!isTaggingActive ? 'disabled' : ''}>
        <span class="icon">⏹️</span>${progress.cancelled ? '正在取消...' : '取消操作'}
      </button>
    </div>

    ${progress.total > 0 ? `
    <div class="progress-container">
      <div class="progress-bar" style="width: ${Math.round((progress.current / progress.total) * 100)}%"></div>
      <div class="progress-text">
        ${progress.current}/${progress.total} (${Math.round((progress.current / progress.total) * 100)}%)
      </div>
    </div>` : ''}

    <div class="log-container" id="log">
      ${progress.total === 0 ? '<div class="empty-state">🖼️ 选择文件后开始智能管理</div>' : ''}
    </div>
  </div>

  <style>
    :root {
      --primary-color: #2c3e50;
      --accent-color: #3498db;
      --warning-color: #e67e22;
      --danger-color: #e74c3c;
    }

    .container {
      padding: 24px;
      max-width: 800px;
      margin: 0 auto;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    }

    .header {
      text-align: center;
      margin-bottom: 2rem;
    }

    .logo {
      width: 64px;
      height: 64px;
      margin-bottom: 1rem;
    }

    .config-group {
      background: #f8f9fa;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 1.5rem;
    }

    .input-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    input[type="number"] {
      padding: 6px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      width: 80px;
    }

    .hint {
      color: #666;
      font-size: 0.9em;
    }

    .control-group {
      display: flex;
      gap: 12px;
      margin: 2rem 0;
      justify-content: center;
    }

    .btn {
      padding: 10px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 500;
    }

    .btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .primary { background: var(--accent-color); color: white; }
    .warning { background: var(--warning-color); color: white; }
    .danger { background: var(--danger-color); color: white; }

    .progress-container {
      height: 28px;
      background: #eee;
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      margin: 2rem 0;
      box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    }

    .progress-bar {
      height: 100%;
      background: linear-gradient(90deg, var(--accent-color), #2980b9);
      transition: width 0.3s ease;
    }

    .progress-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
      font-weight: bold;
      text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    .log-container {
      border: 1px solid #eee;
      border-radius: 8px;
      padding: 16px;
      max-height: 300px;
      overflow-y: auto;
      background: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .log-container div {
      padding: 8px 12px;
      margin: 4px 0;
      background: #f8f9fa;
      border-radius: 4px;
      font-family: monospace;
    }

    .empty-state {
      text-align: center;
      color: #666;
      padding: 2rem !important;
    }

    .icon {
      font-size: 1.1em;
    }
  </style>
`;

// ==================== 功能函数 ====================
function updateChunkSize(value) {
  const size = Math.min(Math.max(parseInt(value), 1), maxChunkSize);
  chunkSize = isNaN(size) ? 16 : size;
}

function confirmForceRefresh() {
  const confirmed = confirm("⚠️ 强制刷新将覆盖现有标签！\n\n确定要继续吗？");
  if (confirmed) handleTagging(true);
}

// ==================== 核心函数 ====================
async function handleTagging(force) {
  if (isTaggingActive) {
    addLog('已有任务进行中，请先取消');
    return;
  }

  try {
    abortController = new AbortController();
    isTaggingActive = true;
    progress = { current: 0, total: 0, cancelled: false };
    updateUI();

    const items = await eagle.item.getSelected();
    const [uris, objs] = processItems(items, force);
    
    if (uris.length === 0) {
      addLog('没有需要处理的文件');
      return;
    }

    progress.total = uris.length;
    updateUI();

    // 使用动态分块大小
    for (let i = 0; i < uris.length; i += chunkSize) {
      if (progress.cancelled) break;

      const chunkUris = uris.slice(i, i + chunkSize);
      const chunkObjs = objs.slice(i, i + chunkSize);

      await processChunk(chunkUris, chunkObjs);
      
      progress.current = Math.min(i + chunkSize, uris.length);
      updateUI();
    }

    addLog(progress.cancelled ? '操作已取消' : '✅ 处理完成');
  } catch (error) {
    addLog(`❌ 错误: ${error.message}`);
  } finally {
    cleanup();
  }
}

// ==================== 工具函数 ====================
async function processChunk(uris, objs) {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/tagger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tag_language: DEFAULT_LANGUAGE,query_uris: uris }),
      signal: abortController.signal
    });

    const { response: results } = await response.json();

    results.forEach((item, index) => {
      objs[index].tags = item.img_tags;
      objs[index].save();
      addLog(`已处理: ${objs[index].name}`);
    });
  } catch (error) {
    if (error.name !== 'AbortError') throw error;
  }
}

function handleCancel() {
  if (isTaggingActive) {
    progress.cancelled = true;
    abortController.abort();
    addLog('正在取消...');
    updateUI();
  }
}
function processItems(items, force) {
  const path = require('path');
  return items.reduce((acc, item) => {
    if (force || item.tags.length === 0) {
      const posixPath = `${eagle.library.path.split(path.sep).join(path.posix.sep)}/images/${item.id}.info/${item.name}.${item.ext}`;
      acc[0].push(posixPath);
      acc[1].push(item);
    } else {
      addLog(`跳过: ${item.name} (已有标签)`);
    }
    return acc;
  }, [[], []]);
}

function addLog(message) {
  const logEl = document.getElementById('log');
  const entry = document.createElement('div');
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  logEl.appendChild(entry);
  logEl.scrollTop = logEl.scrollHeight;
}

function updateUI() {
  document.querySelector('#message').innerHTML = uiTemplate();
}

function cleanup() {
  isTaggingActive = false;
  abortController = null;
  setTimeout(updateUI, 1000);
}

// ==================== 插件初始化 ====================
eagle.onPluginCreate(async (plugin) => {
  document.querySelector('#message').innerHTML = uiTemplate();
});