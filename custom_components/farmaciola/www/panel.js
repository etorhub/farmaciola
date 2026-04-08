const CSS = `
:host {
  display: block;
  padding: 16px;
  background: var(--lovelace-background, var(--primary-background-color));
  min-height: 100vh;
  box-sizing: border-box;
  font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif);
  color: var(--primary-text-color);
}
.header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 16px; flex-wrap: wrap;
}
.title { font-size: 1.3rem; font-weight: 700; flex-shrink: 0; }
.search {
  flex: 1; min-width: 160px;
  background: var(--input-fill-color, var(--secondary-background-color));
  border: 1.5px solid var(--divider-color); border-radius: 999px;
  padding: 8px 16px; font-size: 0.875rem; color: var(--primary-text-color); outline: none;
}
.search:focus { border-color: var(--primary-color); }
.btn-primary {
  background: var(--primary-color); color: var(--text-primary-color);
  border: none; border-radius: 999px; padding: 8px 16px;
  font-size: 0.875rem; font-weight: 600; cursor: pointer; white-space: nowrap;
}
.btn-secondary {
  background: var(--secondary-background-color); color: var(--primary-text-color);
  border: 1.5px solid var(--divider-color); border-radius: 999px;
  padding: 8px 16px; font-size: 0.875rem; font-weight: 600; cursor: pointer;
}
.btn-danger {
  background: var(--error-color, #c62828); color: white; border: none;
  border-radius: 999px; padding: 8px 16px; font-size: 0.875rem; font-weight: 600; cursor: pointer;
}
.med-row {
  display: flex; align-items: center; gap: 12px;
  background: var(--card-background-color); border-radius: 12px;
  padding: 10px 14px; margin-bottom: 8px; cursor: pointer; transition: box-shadow 0.15s;
}
.med-row:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.med-thumb {
  width: 40px; height: 40px; border-radius: 8px; overflow: hidden; flex-shrink: 0;
  background: var(--secondary-background-color); display: flex; align-items: center; justify-content: center;
}
.med-thumb img { width: 100%; height: 100%; object-fit: cover; }
.thumb-ph { font-size: 1.2rem; }
.med-info { flex: 1; min-width: 0; }
.med-name { font-size: 0.875rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.med-sub { font-size: 0.75rem; color: var(--secondary-text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.med-expiry { font-size: 0.75rem; font-weight: 600; flex-shrink: 0; text-align: right; }
.empty { text-align: center; color: var(--secondary-text-color); padding: 40px 20px; }
.link { color: var(--primary-color); cursor: pointer; text-decoration: underline; }
.hidden { display: none !important; }
.stats-bar {
  display: flex; gap: 10px; margin-bottom: 16px;
}
.stat-card {
  flex: 1; background: var(--card-background-color); border-radius: 12px;
  padding: 12px 10px; text-align: center; cursor: pointer;
  border: 2px solid transparent; transition: border-color 0.15s, box-shadow 0.15s;
}
.stat-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.stat-card.active { border-color: var(--primary-color); }
.stat-card.active-warn { border-color: var(--warning-color, #f57f17); }
.stat-card.active-danger { border-color: var(--error-color, #c62828); }
.stat-num { font-size: 1.4rem; font-weight: 700; line-height: 1; }
.stat-num.ok { color: var(--success-color, #43a047); }
.stat-num.warn { color: var(--warning-color, #f57f17); }
.stat-num.danger { color: var(--error-color, #c62828); }
.stat-label { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--secondary-text-color); margin-top: 4px; }
.section-label {
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--primary-color); margin: 12px 0 8px;
}
#modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px;
}
.modal {
  background: var(--card-background-color); border-radius: 20px; padding: 20px;
  width: 100%; max-width: 400px; max-height: 90vh; overflow-y: auto;
}
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.modal-title { font-size: 1rem; font-weight: 700; }
.close-btn { cursor: pointer; color: var(--secondary-text-color); font-size: 1.1rem; }
.mode-toggle {
  display: flex; background: var(--secondary-background-color);
  border-radius: 999px; padding: 3px; margin-bottom: 16px;
}
.mode-btn { flex: 1; text-align: center; padding: 6px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; color: var(--secondary-text-color); cursor: pointer; }
.mode-btn.active { background: var(--card-background-color); color: var(--primary-color); box-shadow: 0 1px 3px rgba(0,0,0,0.15); }
.form-group { margin-bottom: 12px; position: relative; }
.form-label { display: block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--secondary-text-color); margin-bottom: 5px; }
.form-input {
  width: 100%; background: var(--input-fill-color, var(--secondary-background-color));
  border: 1.5px solid var(--divider-color); border-radius: 12px;
  padding: 9px 14px; font-size: 0.875rem; color: var(--primary-text-color); box-sizing: border-box; outline: none;
}
.form-input:focus { border-color: var(--primary-color); }
.ac-dropdown {
  background: var(--card-background-color); border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15); overflow: hidden;
  margin-top: 4px; position: absolute; width: 100%; z-index: 10;
}
.ac-item {
  display: flex; align-items: center; gap: 8px; padding: 8px 12px;
  cursor: pointer; border-bottom: 1px solid var(--divider-color);
}
.ac-item:last-child { border-bottom: none; }
.ac-item:hover { background: var(--secondary-background-color); }
.ac-thumb { width: 32px; height: 32px; border-radius: 6px; flex-shrink: 0; background: var(--secondary-background-color); object-fit: cover; }
.ac-thumb-ph { width: 32px; height: 32px; border-radius: 6px; flex-shrink: 0; background: var(--secondary-background-color); display: flex; align-items: center; justify-content: center; }
.ac-info { flex: 1; min-width: 0; }
.ac-name { font-size: 0.75rem; font-weight: 600; }
.ac-sub { font-size: 0.65rem; color: var(--secondary-text-color); }
.ac-pill { font-size: 0.65rem; background: var(--primary-color); color: var(--text-primary-color); border-radius: 999px; padding: 2px 8px; font-weight: 600; flex-shrink: 0; }
.sel-preview { display: flex; align-items: center; gap: 10px; background: var(--secondary-background-color); border-radius: 12px; padding: 10px 12px; margin-bottom: 14px; }
.sel-thumb { width: 40px; height: 40px; border-radius: 8px; object-fit: cover; }
.sel-thumb-ph { width: 40px; height: 40px; border-radius: 8px; background: var(--divider-color); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; }
.sel-info { flex: 1; min-width: 0; }
.sel-name { font-size: 0.82rem; font-weight: 700; }
.sel-sub { font-size: 0.68rem; color: var(--secondary-text-color); }
.detail-img-wrap { text-align: center; margin-bottom: 12px; }
.detail-img { width: 80px; height: 80px; border-radius: 16px; object-fit: cover; }
.detail-img-ph { width: 80px; height: 80px; border-radius: 16px; background: var(--secondary-background-color); display: inline-flex; align-items: center; justify-content: center; font-size: 2.5rem; }
.detail-name { font-size: 1rem; font-weight: 700; text-align: center; margin-bottom: 2px; }
.detail-sub { font-size: 0.8rem; color: var(--secondary-text-color); text-align: center; margin-bottom: 12px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-bottom: 14px; }
.chip { font-size: 0.68rem; font-weight: 600; border-radius: 999px; padding: 3px 10px; }
.chip-p { background: color-mix(in srgb, var(--primary-color) 15%, transparent); color: var(--primary-color); }
.chip-r { background: color-mix(in srgb, var(--error-color, #c62828) 15%, transparent); color: var(--error-color, #c62828); }
.d-rows { margin-bottom: 14px; }
.d-row { display: flex; justify-content: space-between; align-items: baseline; padding: 7px 0; border-bottom: 1px solid var(--divider-color); font-size: 0.8rem; gap: 8px; }
.d-row:last-child { border-bottom: none; }
.d-row span:first-child { color: var(--secondary-text-color); flex-shrink: 0; }
.d-row span:last-child { font-weight: 600; text-align: right; }
.modal-actions { display: flex; gap: 8px; margin-top: 4px; }
.modal-actions button { flex: 1; }
`;

class FarmaciolaPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._medicines = [];
    this._filter = "";
    this._statFilter = null; // null | "expiring" | "expired"
    this._formMode = "cima";
    this._form = {};
    this._cimaResults = [];
    this._cimaQuery = "";
    this._cimaSelStart = 0;
    this._cimaDebounce = null;
    this._ready = false;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._ready) {
      this._ready = true;
      this._init();
    }
  }

  async _init() {
    this._renderShell();
    await this._loadMedicines();
  }

  async _api(method, path, body) {
    return this._hass.callApi(method, `farmaciola/${path}`, body);
  }

  async _loadMedicines() {
    const list = this.shadowRoot.getElementById("list");
    if (list) list.innerHTML = `<div class="empty">Loading…</div>`;
    try {
      this._medicines = await this._api("GET", "medicines");
    } catch {
      this._medicines = [];
    }
    this._renderStats();
    this._renderList();
  }

  _filtered() {
    let meds = this._medicines;
    if (this._statFilter === "expired") {
      meds = meds.filter((m) => this._expiryStatus(m.fecha_caducidad) === "expired");
    } else if (this._statFilter === "expiring") {
      meds = meds.filter((m) => this._expiryStatus(m.fecha_caducidad) === "expiring");
    }
    if (!this._filter) return meds;
    const q = this._filter.toLowerCase();
    const nameMatch = (m) => (m.nombre || "").toLowerCase().includes(q);
    const descMatch = (m) => [
      m.dosis,
      m.laboratorio,
      m.forma_farmaceutica,
      m.via_administracion,
      ...(m.principios_activos || []),
      m.notas,
    ].some((v) => v && v.toLowerCase().includes(q));
    return meds
      .filter((m) => nameMatch(m) || descMatch(m))
      .sort((a, b) => {
        const an = nameMatch(a), bn = nameMatch(b);
        if (an && !bn) return -1;
        if (!an && bn) return 1;
        return 0;
      });
  }

  _expiryStatus(fecha) {
    if (!fecha) return null;
    const today = new Date();
    const y = today.getFullYear(), m = today.getMonth();
    const exp = new Date(fecha);
    const ey = exp.getFullYear(), em = exp.getMonth();
    if (y > ey || (y === ey && m > em)) return "expired";
    if (y === ey && m === em) return "expiring";
    return "ok";
  }

  _expiryText(fecha) {
    const s = this._expiryStatus(fecha);
    if (s === null) return "—";
    if (s === "expired") return "EXPIRED";
    return new Date(fecha).toLocaleDateString("es-ES", {
      month: "short",
      year: "numeric",
    });
  }

  _expiryColor(fecha) {
    const s = this._expiryStatus(fecha);
    if (s === null) return "var(--secondary-text-color)";
    if (s === "expired") return "var(--error-color, #c62828)";
    if (s === "expiring") return "var(--warning-color, #f57f17)";
    return "var(--success-color, #43a047)";
  }

  _thumbHtml(m, cls = "med-thumb") {
    if (m.foto_url)
      return `<div class="${cls}"><img src="${m.foto_url}" alt="" loading="lazy" /></div>`;
    if (m.foto_manual)
      return `<div class="${cls}"><img src="data:image/jpeg;base64,${m.foto_manual}" alt="" loading="lazy" /></div>`;
    return `<div class="${cls}"><span class="thumb-ph">💊</span></div>`;
  }

  _renderShell() {
    this.shadowRoot.innerHTML = `
      <style>${CSS}</style>
      <div id="app">
        <div class="header">
          <div class="title">Farmaciola 💊</div>
          <input class="search" id="search" type="text" placeholder="Search medicines..." />
          <button class="btn-primary" id="addBtn">+ Add</button>
        </div>
        <div id="stats"></div>
        <div id="list"></div>
        <div id="modal-overlay" class="hidden"></div>
      </div>`;
    this.shadowRoot
      .getElementById("search")
      .addEventListener("input", (e) => {
        this._filter = e.target.value;
        this._renderList();
      });
    this.shadowRoot
      .getElementById("addBtn")
      .addEventListener("click", () => this._openAdd());
    this.shadowRoot
      .getElementById("modal-overlay")
      .addEventListener("click", (e) => {
        if (e.target.id === "modal-overlay") this._closeModal();
      });
  }

  _renderStats() {
    const el = this.shadowRoot.getElementById("stats");
    if (!el) return;
    const total = this._medicines.length;
    const expired = this._medicines.filter((m) => this._expiryStatus(m.fecha_caducidad) === "expired").length;
    const expiring = this._medicines.filter((m) => this._expiryStatus(m.fecha_caducidad) === "expiring").length;
    const sf = this._statFilter;
    el.innerHTML = `
      <div class="stats-bar">
        <div class="stat-card${sf === null ? " active" : ""}" id="sf-all">
          <div class="stat-num ok">${total}</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat-card${sf === "expiring" ? " active-warn" : ""}" id="sf-expiring">
          <div class="stat-num warn">${expiring}</div>
          <div class="stat-label">Expiring</div>
        </div>
        <div class="stat-card${sf === "expired" ? " active-danger" : ""}" id="sf-expired">
          <div class="stat-num danger">${expired}</div>
          <div class="stat-label">Expired</div>
        </div>
      </div>`;
    el.querySelector("#sf-all").addEventListener("click", () => { this._statFilter = null; this._renderStats(); this._renderList(); });
    el.querySelector("#sf-expiring").addEventListener("click", () => { this._statFilter = this._statFilter === "expiring" ? null : "expiring"; this._renderStats(); this._renderList(); });
    el.querySelector("#sf-expired").addEventListener("click", () => { this._statFilter = this._statFilter === "expired" ? null : "expired"; this._renderStats(); this._renderList(); });
  }

  _renderList() {
    const list = this.shadowRoot.getElementById("list");
    const meds = this._filtered();
    const sectionLabel = this._statFilter === "expired"
      ? "Expired medicines"
      : this._statFilter === "expiring"
        ? "Expiring soon (≤ 30 days)"
        : this._medicines.length ? "All medicines" : "";
    const labelHtml = sectionLabel ? `<div class="section-label">${sectionLabel}</div>` : "";
    if (!meds.length) {
      list.innerHTML = labelHtml + `<div class="empty">No medicines found. <span class="link" id="addLink">Add your first one.</span></div>`;
      list
        .querySelector("#addLink")
        ?.addEventListener("click", () => this._openAdd());
      return;
    }
    list.innerHTML = labelHtml + meds
      .map(
        (m) => `
      <div class="med-row" data-id="${m.id}">
        ${this._thumbHtml(m)}
        <div class="med-info">
          <div class="med-name">${m.nombre || "—"}</div>
          <div class="med-sub">${[m.dosis, m.laboratorio].filter(Boolean).join(" · ") || "—"}</div>
        </div>
        <div class="med-expiry" style="color:${m.no_caduca ? 'var(--secondary-text-color)' : this._expiryColor(m.fecha_caducidad)}">${m.no_caduca ? 'Sin caducidad' : this._expiryText(m.fecha_caducidad)}</div>
      </div>`
      )
      .join("");
    list.querySelectorAll(".med-row").forEach((row) => {
      row.addEventListener("click", () => {
        const med = this._medicines.find((m) => m.id === row.dataset.id);
        if (med) this._openDetail(med);
      });
    });
  }

  _ov() {
    return this.shadowRoot.getElementById("modal-overlay");
  }

  _renderDetail(ov, med) {
    ov.innerHTML = `
      <div class="modal">
        <div class="modal-header"><span class="modal-title">Medicine Detail</span><span class="close-btn" id="cls">✕</span></div>
        <div class="detail-img-wrap">
          ${
            med.foto_url
              ? `<img class="detail-img" src="${med.foto_url}" alt="" loading="lazy" />`
              : med.foto_manual
                ? `<img class="detail-img" src="data:image/jpeg;base64,${med.foto_manual}" alt="" />`
                : `<div class="detail-img-ph">💊</div>`
          }
        </div>
        <div class="detail-name">${med.nombre || "—"}</div>
        <div class="detail-sub">${med.forma_farmaceutica || ""}</div>
        <div class="chips">
          ${med.via_administracion ? `<span class="chip chip-p">${med.via_administracion}</span>` : ""}
          ${med.dosis ? `<span class="chip chip-p">${med.dosis}</span>` : ""}
          ${med.prescripcion ? `<span class="chip chip-r">Prescription required</span>` : ""}
        </div>
        <div class="d-rows">
          <div class="d-row"><span>Active ingredients</span><span>${(med.principios_activos || []).join(", ") || "—"}</span></div>
          <div class="d-row"><span>Lab</span><span>${med.laboratorio || "—"}</span></div>
          <div class="d-row"><span>Expiry</span><span style="color:${med.no_caduca ? 'var(--secondary-text-color)' : this._expiryColor(med.fecha_caducidad)}">${med.no_caduca ? 'Sin caducidad' : (med.fecha_caducidad ? new Date(med.fecha_caducidad).toLocaleDateString("es-ES", { month: "long", year: "numeric" }) : "—")}</span></div>
          <div class="d-row"><span>Notes</span><span>${med.notas || "—"}</span></div>
        </div>
        <div class="modal-actions">
          <button class="btn-danger" id="delBtn">🗑 Delete</button>
          <button class="btn-primary" id="editBtn">✏️ Edit</button>
        </div>
      </div>`;
    ov.querySelector("#cls").addEventListener("click", () => this._closeModal());
    ov.querySelector("#delBtn").addEventListener("click", () => this._delete(med.id));
    ov.querySelector("#editBtn").addEventListener("click", () => this._openEdit(med));
  }

  async _openDetail(med) {
    const ov = this._ov();
    ov.classList.remove("hidden");
    // Render immediately with data we have; fetch full record (incl. foto_manual) in background
    this._renderDetail(ov, med);
    if (med.has_foto_manual && !med.foto_manual) {
      try {
        const full = await this._api("GET", `medicines/${med.id}`);
        // Patch local cache so edit form also gets the photo
        const idx = this._medicines.findIndex((m) => m.id === med.id);
        if (idx !== -1) this._medicines[idx] = { ...this._medicines[idx], foto_manual: full.foto_manual };
        // Update image if modal is still open for this medicine
        const wrap = ov.querySelector(".detail-img-wrap");
        if (wrap && full.foto_manual) {
          wrap.innerHTML = `<img class="detail-img" src="data:image/jpeg;base64,${full.foto_manual}" alt="" />`;
        }
        med = full;
        ov.querySelector("#editBtn").replaceWith(ov.querySelector("#editBtn").cloneNode(true));
        ov.querySelector("#editBtn").addEventListener("click", () => this._openEdit(med));
      } catch { /* show without photo */ }
    }
  }

  _openAdd() {
    this._form = { source: "cima" };
    this._formMode = "cima";
    this._cimaResults = [];
    this._cimaQuery = "";
    this._cimaSelStart = 0;
    this._renderForm(null);
  }

  _openEdit(med) {
    this._form = { ...med };
    this._formMode = med.source === "cima" ? "cima" : "manual";
    this._cimaResults = [];
    this._renderForm(med);
  }

  _renderForm(editing) {
    const isEdit = editing !== null;
    const ov = this._ov();
    ov.classList.remove("hidden");
    const cimaSelected = this._formMode === "cima" && this._form.nregistro;

    ov.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <span class="modal-title">${isEdit ? "Edit Medicine" : "Add Medicine"}</span>
          <span class="close-btn" id="cls">✕</span>
        </div>
        <div class="mode-toggle">
          <div class="mode-btn ${this._formMode === "cima" ? "active" : ""}" id="mCI">🔍 CIMA Search</div>
          <div class="mode-btn ${this._formMode === "manual" ? "active" : ""}" id="mMN">✏️ Manual</div>
        </div>
        ${
          this._formMode === "cima"
            ? cimaSelected
              ? `<div class="sel-preview">
              ${this._form.foto_url ? `<img class="sel-thumb" src="${this._form.foto_url}" />` : `<div class="sel-thumb-ph">💊</div>`}
              <div class="sel-info">
                <div class="sel-name">${this._form.nombre}</div>
                <div class="sel-sub">${[this._form.dosis, this._form.laboratorio].filter(Boolean).join(" · ")}</div>
              </div>
              <span class="link" id="chgBtn">Change</span>
            </div>`
              : `<div class="form-group">
              <label class="form-label">Medicine name</label>
              <input class="form-input" id="cimaQ" type="text" placeholder="Type to search CIMA..." autocomplete="off" />
              <div id="acDrop" class="ac-dropdown ${this._cimaResults.length ? "" : "hidden"}">
                ${this._cimaResults
                  .map(
                    (r) => `
                  <div class="ac-item" data-nr="${r.nregistro}">
                    ${r.foto_url ? `<img class="ac-thumb" src="${r.foto_url}" />` : `<div class="ac-thumb-ph">💊</div>`}
                    <div class="ac-info"><div class="ac-name">${r.nombre}</div><div class="ac-sub">${[r.forma_farmaceutica, r.laboratorio].filter(Boolean).join(" · ")}</div></div>
                    ${r.dosis ? `<span class="ac-pill">${r.dosis}</span>` : ""}
                  </div>`
                  )
                  .join("")}
              </div>
            </div>`
            : `<div class="form-group"><label class="form-label">Name *</label><input class="form-input" id="mName" type="text" value="${this._form.nombre || ""}" /></div>
          <div class="form-group"><label class="form-label">Dosage</label><input class="form-input" id="mDosis" type="text" value="${this._form.dosis || ""}" /></div>
          <div class="form-group"><label class="form-label">Pharmaceutical form</label><input class="form-input" id="mForma" type="text" value="${this._form.forma_farmaceutica || ""}" /></div>
          <div class="form-group"><label class="form-label">Photo (optional)</label><input class="form-input" id="mPhoto" type="file" accept="image/*" /></div>`
        }
        <div class="form-group" id="expiryRow"${this._form.no_caduca ? ' style="display:none"' : ''}><label class="form-label">Expiry date *</label><input class="form-input" id="expiry" type="month" value="${this._form.fecha_caducidad ? this._form.fecha_caducidad.substring(0, 7) : ""}" /></div>
        <div class="form-group"><label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:0.875rem"><input type="checkbox" id="noCaduca"${this._form.no_caduca ? ' checked' : ''}> Sin fecha de caducidad</label></div>
        <div class="form-group"><label class="form-label">Notes</label><input class="form-input" id="notes" type="text" placeholder="Optional..." value="${this._form.notas || ""}" /></div>
        <div class="modal-actions">
          <button class="btn-secondary" id="cancelBtn">Cancel</button>
          <button class="btn-primary" id="saveBtn">${isEdit ? "Save changes" : "Add medicine"}</button>
        </div>
      </div>`;

    ov.querySelector("#cls").addEventListener("click", () =>
      this._closeModal()
    );
    ov.querySelector("#cancelBtn").addEventListener("click", () =>
      this._closeModal()
    );
    ov.querySelector("#mCI")?.addEventListener("click", () => {
      this._formMode = "cima";
      this._cimaResults = [];
      this._renderForm(editing);
    });
    ov.querySelector("#mMN")?.addEventListener("click", () => {
      this._formMode = "manual";
      this._renderForm(editing);
    });
    ov.querySelector("#chgBtn")?.addEventListener("click", () => {
      this._form = { source: "cima" };
      this._cimaQuery = "";
      this._cimaSelStart = 0;
      this._cimaResults = [];
      this._renderForm(editing);
    });
    ov.querySelectorAll(".ac-item").forEach((item) =>
      item.addEventListener("click", () =>
        this._selectCima(item.dataset.nr, editing)
      )
    );
    const cimaInput = ov.querySelector("#cimaQ");
    if (cimaInput) {
      cimaInput.value = this._cimaQuery;
      cimaInput.focus();
      cimaInput.setSelectionRange(this._cimaSelStart, this._cimaSelStart);
      cimaInput.addEventListener("input", (e) => {
        this._cimaQuery = e.target.value;
        this._cimaSelStart = e.target.selectionStart;
        clearTimeout(this._cimaDebounce);
        const drop = ov.querySelector("#acDrop");
        if (this._cimaQuery.length < 2) {
          this._cimaResults = [];
          if (drop) {
            drop.classList.add("hidden");
            drop.innerHTML = "";
          }
          return;
        }
        this._cimaDebounce = setTimeout(
          () => this._searchCima(editing),
          300
        );
      });
    }
    const noCaducaEl = ov.querySelector("#noCaduca");
    const expiryRow = ov.querySelector("#expiryRow");
    noCaducaEl?.addEventListener("change", () => {
      expiryRow.style.display = noCaducaEl.checked ? "none" : "";
    });
    ov.querySelector("#saveBtn").addEventListener("click", () =>
      this._save(editing)
    );
  }

  async _searchCima(editing) {
    try {
      this._cimaResults = await this._api(
        "GET",
        `cima/search?q=${encodeURIComponent(this._cimaQuery)}`
      );
    } catch {
      this._cimaResults = [];
    }
    const drop = this._ov()?.querySelector("#acDrop");
    if (drop) this._updateDrop(drop, editing);
  }

  _updateDrop(drop, editing) {
    if (!this._cimaResults.length) {
      drop.classList.add("hidden");
      drop.innerHTML = "";
      return;
    }
    drop.classList.remove("hidden");
    drop.innerHTML = this._cimaResults
      .map(
        (r) => `
      <div class="ac-item" data-nr="${r.nregistro}">
        ${r.foto_url ? `<img class="ac-thumb" src="${r.foto_url}" />` : `<div class="ac-thumb-ph">💊</div>`}
        <div class="ac-info"><div class="ac-name">${r.nombre}</div><div class="ac-sub">${[r.forma_farmaceutica, r.laboratorio].filter(Boolean).join(" · ")}</div></div>
        ${r.dosis ? `<span class="ac-pill">${r.dosis}</span>` : ""}
      </div>`
      )
      .join("");
    drop.querySelectorAll(".ac-item").forEach((item) =>
      item.addEventListener("click", () =>
        this._selectCima(item.dataset.nr, editing)
      )
    );
  }

  async _selectCima(nregistro, editing) {
    try {
      const detail = await this._api(
        "GET",
        `cima/medicamento?nregistro=${nregistro}`
      );
      this._form = { ...this._form, ...detail, source: "cima" };
    } catch {
      /* keep form */
    }
    this._renderForm(editing);
  }

  async _save(editing) {
    const ov = this._ov();
    const noCaduca = ov.querySelector("#noCaduca")?.checked || false;
    const expiryVal = ov.querySelector("#expiry")?.value;
    if (!noCaduca && !expiryVal) {
      alert("Indica la fecha de caducidad o marca 'Sin fecha de caducidad'");
      return;
    }
    const fecha_caducidad = noCaduca ? null : expiryVal + "-01";
    const notas = ov.querySelector("#notes")?.value || "";
    let body;
    if (this._formMode === "cima") {
      if (!this._form.nregistro && !editing) {
        alert("Please select a medicine from CIMA");
        return;
      }
      body = { ...this._form, fecha_caducidad, no_caduca: noCaduca, notas };
    } else {
      const nombre = ov.querySelector("#mName")?.value?.trim();
      if (!nombre) {
        alert("Name is required");
        return;
      }
      body = {
        source: "manual",
        nombre,
        dosis: ov.querySelector("#mDosis")?.value || "",
        forma_farmaceutica: ov.querySelector("#mForma")?.value || "",
        fecha_caducidad,
        no_caduca: noCaduca,
        notas,
      };
      const file = ov.querySelector("#mPhoto")?.files?.[0];
      if (file) body.foto_manual = await this._toBase64(file);
    }
    try {
      if (editing) {
        await this._api("PUT", `medicines/${editing.id}`, body);
      } else {
        await this._api("POST", "medicines", body);
      }
      this._closeModal();
      await this._loadMedicines();
    } catch {
      alert("Error saving medicine. Please try again.");
    }
  }

  async _delete(id) {
    if (!confirm("Delete this medicine?")) return;
    try {
      await this._api("DELETE", `medicines/${id}`);
      this._closeModal();
      await this._loadMedicines();
    } catch {
      alert("Error deleting medicine.");
    }
  }

  _closeModal() {
    const ov = this._ov();
    ov.classList.add("hidden");
    ov.innerHTML = "";
    this._cimaResults = [];
    this._cimaQuery = "";
    this._cimaSelStart = 0;
  }

  _toBase64(file) {
    return new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = (e) => res(e.target.result.split(",")[1]);
      r.onerror = rej;
      r.readAsDataURL(file);
    });
  }
}

customElements.define("farmaciola-panel", FarmaciolaPanel);
