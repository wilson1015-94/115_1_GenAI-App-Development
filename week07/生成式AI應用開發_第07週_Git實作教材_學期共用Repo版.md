# Git 與 GitHub 實作教材｜第 7 週起通用

本講義適用於第 7 週起的課堂實作、作業保存與專題開發。每位學生整學期使用自己的 **`115_1_GenAI-APP-Development`** Repo，每週加入老師提供的教材，完成當週要求後 Commit、Push。

建立 Repo 後，透過老師另外提供的 **Google 表單**登記自己的 Repo 首頁連結。老師從已登記的 Repo 查看各週進度，<font color="#C62828"><b>不需要每週另外繳交資料夾連結。</b></font>

第 7 週僅作為下載、資料夾與部署路徑的例子。<font color="#C62828"><b>當週的程式內容、TODO、Python 版本、套件與完成標準，請依當週 README 及老師公告操作。</b></font>

色彩提示：<font color="#C62828"><b>紅色＝重要觀念與限制</b></font>；<font color="#1565C0"><b>藍色＝操作提示</b></font>；<font color="#2E7D32"><b>綠色＝預期觀察與完成證據</b></font>。

閱讀提示：在 VS Code 按 Ctrl+Shift+V 預覽本講義；部分閱讀平台可能移除 HTML 顏色，仍可依粗體與標籤閱讀。

## 一、每週都使用的流程

```text
登入自己的帳號
    ↓
這台電腦沒有自己的 Repo → Clone
這台電腦已有自己的 Repo → 確認進度後 Fetch／Pull
    ↓
從老師教材 Repo 下載最新版 ZIP
    ↓
只複製當週資料夾到自己的 Repo
    ↓
檢查忽略規則 → Commit／Push 保存教材起點
    ↓
依當週 README 準備環境、聽講與完成作業
    ↓
檢查修改 → Commit → Push → GitHub 網頁確認
    ↓
老師從已登記的 Repo 查看進度；需要部署時再設定雲端 App
```

<font color="#C62828"><b>Commit 只記錄在本機，Push 後才會出現在 GitHub。</b></font> 每次離開教室或換電腦前，都要到 GitHub 網頁確認最新進度。

## 二、分清楚教材來源與自己的作業 Repo

老師提供的公開教材來源：[115_1_GenAI-App-Development-Student](https://github.com/shuochenghu/115_1_GenAI-App-Development-Student)。

```text
https://github.com/shuochenghu/115_1_GenAI-App-Development-Student.git
```

| 用途 | Repo | 學生操作 |
|---|---|---|
| 教材來源 | `shuochenghu/115_1_GenAI-App-Development-Student` | 下載老師提供的教材 |
| 自己的作業 | `自己的帳號/115_1_GenAI-APP-Development` | 表單登記 Repo、Clone／Pull、完成作業、Commit／Push 與部署 |

<font color="#C62828"><b>老師的 Repo 用來取得教材；自己的 Repo 才是實作、保存與供老師檢視的位置。</b></font> 對自己的 Repo 做 Pull，不會自動取得老師教材 Repo 的新內容。

| 名詞 | 用一句話理解 |
|---|---|
| Repository（Repo） | 受 Git 管理的專案資料夾與版本歷史 |
| Clone | 從 GitHub 建立本機副本，包含歷史與遠端連線 |
| Fetch／Pull | 查詢遠端更新，並將新提交同步至既有本機副本 |
| Commit | 把選取的變更記錄成本機版本 |
| Push | 將本機提交上傳至自己的 GitHub Repo |
| `.gitignore` | 指定不納入追蹤的本機設定與生成檔案 |
| `README.md` | 說明操作方式、作業內容與實際驗證結果 |

## 三、第一次使用：建立並 Clone 自己的 Repo

### 3-1 前置確認

- [ ] 能登入自己的 GitHub 帳號。
- [ ] GitHub Desktop 已安裝並登入自己的帳號。
- [ ] VS Code 已安裝；當週所需工具依 README 準備。
- [ ] 能開啟老師的公開教材 Repo。
- [ ] 知道自己的本機存放位置與老師公告的 Google 表單登記方式。

共用電腦請使用自己的資料夾，不接續同學遺留的 Repo。帳號或工具尚未準備好時，可參考 [GitHub](https://github.com) 與 [GitHub Desktop](https://desktop.github.com)。

### 3-2 在 GitHub 建立 Repo（整學期只做一次）

登入 GitHub，選 <font color="#1565C0"><b>＋ → New repository</b></font>：

| 欄位 | 設定 |
|---|---|
| Owner | 自己的 GitHub 帳號 |
| Repository name | `115_1_GenAI-APP-Development` |
| Description | 生成式 AI 應用開發：課堂實作與作業 |
| Visibility | 課堂建議 Public；若使用 Private，依老師指定方式提供檢視權限 |
| Add README | 勾選 |
| Add .gitignore | 選擇 Python，稍後補上課程忽略規則 |

按 **Create repository**。已有同名 Repo 就直接使用，不必每週建立新的 Repo。

### 3-3 用 GitHub Desktop Clone

1. 選 <font color="#1565C0"><b>File → Clone repository</b></font>。
2. 選自己帳號下的 `115_1_GenAI-APP-Development`；未列出時，在 URL 分頁貼上自己的 Repo 網址。
3. 確認 Local path 最後一層是自己的 Repo 名稱，位置可寫入。
4. 按 **Clone**，再選 <font color="#1565C0"><b>Repository → Open in Visual Studio Code</b></font>。

<font color="#2E7D32"><b>預期觀察：</b></font> VS Code 開啟自己的作業 Repo，根目錄可看到 `README.md` 與 `.gitignore`。

<font color="#C62828"><b>自己的作業 Repo 使用 Clone，老師的教材來源則下載 ZIP。</b></font> ZIP 不含可接續使用的 Git 歷史與遠端連線。可回查 [GitHub Desktop 官方 Clone 說明](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop)。

### 3-4 透過 Google 表單登記自己的 Repo

老師會另外公告 Google 表單連結。首次建立 Repo 後，在表單填寫自己的 **Repo 首頁網址**，格式如下，把 `你的帳號` 換成自己的 GitHub 帳號：

```text
https://github.com/你的帳號/115_1_GenAI-APP-Development
```

1. 在 GitHub 開啟自己的作業 Repo 首頁，複製網址。
2. 打開老師提供的 Google 表單，依表單要求填寫並送出。
3. 確認填的是自己的 Repo，並確認老師能開啟；Private 作業 Repo 須依公告提供檢視權限。

<font color="#2E7D32"><b>完成證據：</b></font> 表單已登記正確的 Repo 首頁連結，老師可由此找到各週資料夾與提交紀錄。

<font color="#C62828"><b>整學期沿用同一個 Repo，不必每週重填表單或另交資料夾連結。</b></font> 不要填成老師的教材來源、單一檔案、週次資料夾或 App 網址。Repo 網址若有變更，依老師公告更新登記。

## 四、每次上課：先同步自己的進度

這台電腦已有自己的副本時，不用重新 Clone：

1. 確認 GitHub Desktop 的 Current repository 是自己的作業 Repo，Branch 是 `main`。
2. 查看 Changes 與尚未 Push 的提交，確認沒有未處理的工作。
3. 按 <font color="#1565C0"><b>Fetch origin</b></font>；出現 **Pull origin** 時按下同步。
4. 到 VS Code 確認當週要使用的資料夾與檔案。

若本機仍有自己的修改，先檢查並保存，再同步遠端。遇到不明變更、衝突或其他人的檔案，請老師協助；<font color="#C62828"><b>不要直接丟棄變更或強制覆寫。</b></font>

<font color="#2E7D32"><b>預期觀察：</b></font> 本機可看到其他電腦已 Push 的最新提交。Pull 取得的是自己 GitHub 上的進度，接下來仍須另外下載老師的新教材。

## 五、每週取得教材並放進自己的 Repo

### 5-1 下載老師的教材

1. 開啟上面的教材來源 Repo。
2. 在 Repo 根目錄按 <font color="#1565C0"><b>Code → Download ZIP</b></font>。
3. 將 ZIP 解壓縮到自己的作業 Repo 以外，例如「下載」資料夾。
4. 找到老師公告的當週資料夾，保留裡面的程式、README、套件清單、範例設定與練習資料。

外層解壓縮資料夾通常包含來源 Repo 名稱與下載分支名稱，不是要放進作業 Repo 的每週資料夾。

### 5-2 複製的位置：以第 7 週為例

下表只示範來源與目的位置如何對應，其他週次依老師公告的名稱操作。

| 項目 | 第 7 週路徑範例 |
|---|---|
| 老師教材 Repo 內的來源 | `week07/` |
| 學生自己 Repo 內的目的位置 | `week07-streamlit-app/` |
| 一個程式的位置 | `week07-streamlit-app/student/01_inputs.py` |

把來源 `week07/` 複製到自己的 Repo 根目錄，再將複製後的資料夾命名為 `week07-streamlit-app/`。

```text
115_1_GenAI-APP-Development/
├── README.md                      ← 整學期作業索引
├── .gitignore                     ← 整個 Repo 共用的忽略規則
├── week07-streamlit-app/           ← 第 7 週路徑範例
│   ├── README.md
│   ├── requirements.txt
│   └── student/
│       └── 01_inputs.py           ← 只示範程式路徑
└── 其他週次的資料夾/               ← 名稱與內容依老師公告
```

<font color="#C62828"><b>只複製指定週次，不把整個教材來源 Repo 放進自己的 Repo。</b></font> 不要帶入來源的 `.git/`，也不要用來源根目錄的 README 或 `.gitignore` 覆蓋自己的設定。避免多套一層同名資料夾。

複製資料時不要帶入別人的虛擬環境、真實金鑰或教師答案。若同週資料夾已存在，先依第八節保存進度、比較差異，不直接整包覆蓋。

<font color="#2E7D32"><b>預期觀察：</b></font> GitHub Desktop 的 Changes 顯示新加入的當週檔案，Current repository 仍是自己的作業 Repo。

### 5-3 檢查忽略規則

在自己的 Repo 根目錄打開 `.gitignore`，保留既有 Python 模板，補上以下規則：

```gitignore
# 本機金鑰與環境設定；保留可公開的範例檔
.env
.env.*
!.env.example
!.env.*.example
**/.streamlit/secrets.toml

# 各週自行建立的環境與暫存檔
.venv/
.venv-*/
venv/
__pycache__/
*.pyc
.apptest-temp/
.DS_Store
Thumbs.db
```

每次提交前，都要確認真實 `.env`、`secrets.toml`、虛擬環境與暫存檔不在 Changes。範例設定檔可提交，但只能放占位值。

<font color="#C62828"><b>忽略規則只對尚未追蹤的檔案生效，不能消除既有提交中的金鑰。</b></font>

### 5-4 保存當週教材起點

1. 在 GitHub Desktop 檢查新增檔案與差異，確認是本週教材。
2. Summary 寫明週次與動作，例如 `第7週：匯入課堂教材`。
3. 按 <font color="#1565C0"><b>Commit to main</b></font>，再按 **Push origin**。
4. 到 GitHub 網頁確認當週資料夾已上傳。

<font color="#2E7D32"><b>完成證據：</b></font> GitHub 留下一筆教材起點，之後可比較自己的修改。<font color="#C62828"><b>匯入教材的 Commit 不代表已完成作業。</b></font>

## 六、依當週要求實作，再保存修改

### 6-1 準備環境與進行課堂實作

在 VS Code 讀取當週 `README.md`，依說明選擇 Python 版本、建立或啟用環境、安裝套件及啟動程式。各週使用的版本、入口檔案與設定位置可能不同，依當週文件操作。

老師提供 `student/` 時，在指定的學生檔案完成 TODO；個人專題則依當週規格設計與驗收。Git 講義負責保存與同步流程，作業內容及測試方法由當週教材說明。

<font color="#C62828"><b>Clone 不會帶回被忽略的虛擬環境與金鑰設定。</b></font> 換電腦後須依 README 重建環境，私下設定金鑰；不要把整份虛擬環境拷到不同電腦。

### 6-2 保存自己的作業

1. 儲存檔案，依當週要求操作並檢查結果。
2. 回 GitHub Desktop，逐一查看 Changes，確認自己的修改與準備提交的檔案。
3. 排除金鑰、不明檔案與不應提交的生成內容。
4. 完成一項有意義的工作就 Commit，例如 `第7週：完成課堂練習並檢查結果`、`修正：處理空白輸入`。
5. 按 <font color="#1565C0"><b>Push origin</b></font>，等待完成。
6. 到 GitHub 網頁確認最新提交與檔案內容。

每週保留「教材起點」與「自己的實作」兩個階段。不必為湊次數製造修改，也不要只提交匯入的教材。

### 6-3 更新當週 README，供老師檢視進度

保留老師提供的操作說明，加入自己的簡短紀錄：

| 項目 | 記錄內容 |
|---|---|
| 作業完成情形 | 完成、部分完成或未完成的項目，以及自己的修改 |
| 啟動方式 | 實際資料夾、命令、環境與必要設定 |
| 驗證結果 | 測試輸入、操作、實際結果、問題與未測項目 |
| AI 協助 | 工具、協助內容、自己修改與親自驗證事項；未使用則註明 |
| 部署 | 當週有要求或自行選做時，附網址與實際驗證結果 |

<font color="#C62828"><b>實測與未測項目要分開記錄，不能把固定示範或假回應當成真實 API 成果。</b></font> 不在程式、README 或截圖中放真實金鑰與個資。

每週仍須依老師公告的進度與期限完成實作，更新當週資料夾與 README，Commit、Push 並在 GitHub 網頁確認。老師從 Google 表單已登記的 Repo 查看進度，學生不需另外繳交當週資料夾連結。

根目錄 README 可加入作業索引，例如 `[第7週作業](week07-streamlit-app/)`，方便老師找到各週內容。當週有部署要求時，依公告提供 App 網址與驗證紀錄；程式與紀錄仍保存在同一個 Repo。

## 七、離開教室與回家接續

| 時機 | 操作 |
|---|---|
| 離開目前電腦前 | 儲存 → 檢查 → Commit → Push → GitHub 網頁確認 |
| 到另一台電腦第一次工作 | Clone 自己的 Repo → 依當週 README 準備環境 |
| 另一台電腦已有自己的副本 | 確認本機進度 → Fetch／Pull → 啟用正確環境 |
| 回教室繼續 | 先同步自己在家已 Push 的進度，再開始修改 |

<font color="#C62828"><b>只做 Commit 就離開，另一台電腦無法從 GitHub 取得這筆尚未 Push 的進度。</b></font>

共用電腦離開前，依教室規定登出 GitHub、Desktop 與部署平台，並處理本機私密設定。

## 八、下一週教材與同週修正

新的一週沿用同一個 Repo，加入新的週次資料夾，保留之前的作業與歷史。

老師補發同週修正時：

1. 先保存並 Push 自己目前的進度。
2. 重新下載老師公告的教材版本，解壓縮到作業 Repo 以外。
3. 依老師公告比較指定檔案，只合併需要的更新。
4. 保留自己已完成的作業，重新檢查後 Commit、Push。

<font color="#C62828"><b>不要整包覆蓋已完成的 TODO，也不要用重新下載教材取代作業同步。</b></font> 無法判斷差異時，先請老師協助。

## 九、需要部署時：從自己的 Repo 選擇入口

是否部署及如何提供 App 網址依當週公告；學期作業 Repo 仍以 Google 表單登記的連結為準。以下說明 Streamlit Community Cloud 的通用設定，第 7 週檔名只作為路徑例子，不涉及該程式的功能與練習內容。

### 9-1 先確認入口與套件清單

找出當週 README 指定的入口檔案。部署使用「Repo＋分支＋入口路徑」，不要求所有週次都叫 `app.py` 或都放在 `student/`。

| 設定 | 第 7 週路徑範例 | 其他週次怎麼換 |
|---|---|---|
| Repository | `你的帳號/115_1_GenAI-APP-Development` | 沿用自己的學期 Repo |
| Branch | `main` | 使用保存作業的分支 |
| Main file path | `week07-streamlit-app/student/01_inputs.py` | 替換為當週入口相對於 Repo 根目錄的完整路徑 |

<font color="#C62828"><b>部署路徑使用 /，不要使用 Windows 的反斜線。</b></font> 一個部署指定一個入口；多個 `.py` 不會自動變成網站的多個頁面。

Cloud 先找入口同層，再找 Repo 根目錄的套件清單。本例的 `requirements.txt` 若只位於 `week07-streamlit-app/`，不會因它在入口上層就自動找到。見 [官方套件搜尋規則](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)。

可依老師指定的方式處理：

- 入口與 `requirements.txt` 在同一資料夾時，直接保留這個配置。
- 入口在更深的子資料夾時，可由老師提供相符的 Repo 根目錄清單，或在入口同層提供該 App 的清單。

以下命令只示範「根目錄尚無套件清單，且老師指定使用共用清單」的情況，從自己的 Repo 根目錄執行：

```powershell
Copy-Item .\week07-streamlit-app\requirements.txt .\requirements.txt
```

<font color="#C62828"><b>不要每週無條件覆蓋根目錄的套件清單。</b></font> 各週需求不同時要分別確認，避免影響其他已部署 App。套件清單可提交，虛擬環境與金鑰不提交。

### 9-2 以相同啟動位置檢查，再 Push

先依當週 README 啟用正確環境，從自己的 Repo 根目錄測試入口。以下只示範第 7 週路徑：

```powershell
python -m streamlit run week07-streamlit-app/student/01_inputs.py
```

Cloud 從 Repo 根目錄啟動，本機也從這裡檢查，可提早發現檔案路徑問題。完成檢查後，將入口、必要資料與套件清單 Commit、Push。見 [官方檔案配置說明](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)。

### 9-3 在平台建立 App

1. 到 [Streamlit Community Cloud](https://share.streamlit.io) 登入，授權存取自己的 GitHub Repo。
2. 選 <font color="#1565C0"><b>Create app</b></font>，選擇部署已有的 App。
3. 填入自己的 Repo、分支與當週入口路徑。
4. 在 <font color="#1565C0"><b>Advanced settings</b></font> 選擇老師已驗證的 Python 版本；需要金鑰時設定 Secrets。
5. 儲存後按 **Deploy**，查看部署紀錄，完成後開啟網址驗證。

本機與 Cloud 的 Python、套件及執行環境都需確認；本機能啟動不代表已完成雲端驗證。介面與完整操作可回查 [官方部署說明](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)。

### 9-4 金鑰與更新

當週程式需要 API 時，依 README 的設定名稱與讀取方式，在平台 Secrets 填入設定。例如使用 `OPENAI_API_KEY`：

```toml
OPENAI_API_KEY = "填入你自己的API金鑰"
```

本機依當週 README 使用 `.env` 或本機 Secrets，Cloud 則在平台設定；<font color="#C62828"><b>真實金鑰不經 GitHub 上傳，也不會隨 Clone 自動帶回。</b></font> 平台頂層 Secrets 可提供為環境變數，仍須與程式讀取方式一致。見 [官方 Secrets 說明](https://docs.streamlit.io/develop/concepts/connections/secrets-management)。

之後修改已部署程式，Commit、Push 到該 App 指定分支，再開啟網址確認平台更新。不要以固定等待秒數當作完成證據。若 App 使用部署者金鑰，訪客操作可能產生請求；公開方式與使用限制依當週規範處理，API 勾選框本身不是存取控制。

<font color="#2E7D32"><b>完成證據：</b></font> 網址可開啟，當週要求的操作已實際檢查，README 記錄結果與未測項目。只有部署成功訊息，不能取代功能與內容驗證。

## 十、常見問題與版本回復

| 問題 | 先檢查什麼 |
|---|---|
| 老師教材網頁顯示 404 | 網址是否正確、老師是否已完成公開設定 |
| Clone 或 Push 失敗 | 自己的帳號、Repo 網址、網路與權限 |
| Changes 沒有修改 | 是否儲存、是否選對 Repo、是否改到 Repo 外的另一份檔案 |
| 換電腦看不到進度 | 前一台是否已 Push，這台是否 Fetch／Pull |
| Clone 後不能啟動 | 是否依當週 README 重建環境與本機設定 |
| 金鑰或虛擬環境出現在 Changes | 根目錄忽略規則是否正確，檔案是否已被追蹤 |
| Cloud 找不到程式或套件 | 入口路徑、分支、大小寫、套件清單位置與 Push 狀態 |
| Cloud 顯示缺少設定 | Secrets 名稱、格式及程式讀取方式是否一致 |

在 GitHub Desktop 的 <font color="#1565C0"><b>History</b></font> 選取提交，可以查看當次差異。需要取消某筆提交時，先保存目前進度，再請老師協助判斷是否使用 **Revert Changes in Commit**。

Revert 會新增一筆反向修改，並非直接回到所選提交當時的完整版本；取消較早的提交也可能和後續修改衝突。

若真實金鑰曾被 Commit 或 Push，立即到服務提供者後台撤銷並重新建立，請老師協助停止追蹤與清理歷史。<font color="#C62828"><b>事後補忽略規則、刪檔或 Revert，都不能消除歷史中的金鑰。</b></font>

## 十一、每週進度確認

- [ ] Current repository 是自己的學期作業 Repo。
- [ ] 首次建立後已透過老師的 Google 表單登記 Repo 首頁連結；網址未變更就不必重填。
- [ ] 當週資料夾位置與名稱符合公告，沒有多套一層資料夾。
- [ ] 依當週 README 完成指定實作，保留自己的修改與紀錄。
- [ ] 真實金鑰、虛擬環境與不應提交的資料未納入追蹤。
- [ ] 留下教材起點與自己的實作 Commit，能說明差異。
- [ ] <font color="#2E7D32"><b>已 Push，並在 GitHub 網頁確認最新程式。</b></font>
- [ ] README 寫明操作方式、完成情形、實測與未測項目。
- [ ] 老師可從已登記的 Repo 找到當週資料夾；有部署要求時依公告提供 App 網址與驗證紀錄。
- [ ] 離開共用電腦前依教室規定處理帳號與本機私密設定。

## 附錄：常用操作對照

| 動作 | 命令列（選讀） | GitHub Desktop |
|---|---|---|
| 取得自己的本機副本 | `git clone <自己的Repo網址>` | File → Clone repository |
| 查看變更 | `git status`、`git diff` | Changes 與右側差異 |
| 選取要記錄的檔案 | `git add <檔案路徑>` | 在 Changes 勾選檔案 |
| 記錄版本 | `git commit -m "具體說明"` | 填 Summary → Commit to main |
| 上傳提交 | `git push` | Push origin |
| 查詢與下載更新 | `git fetch`，確認後 `git pull` | Fetch origin → Pull origin |
| 查看歷史 | `git log` | History |
| 取消指定提交的修改 | `git revert <提交編號>` | History → Revert Changes in Commit |
