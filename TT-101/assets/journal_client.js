(function(){
  const KEY = 'TT_JOURNAL_ENTRIES_V1';
  function load(){
    try{ return JSON.parse(localStorage.getItem(KEY) || '[]'); }catch(e){ return []; }
  }
  function save(arr){
    localStorage.setItem(KEY, JSON.stringify(arr));
  }
  async function sha256Hex(str){
    const enc = new TextEncoder().encode(str);
    const buf = await crypto.subtle.digest('SHA-256', enc);
    const bytes = Array.from(new Uint8Array(buf));
    return bytes.map(b=>b.toString(16).padStart(2,'0')).join('');
  }
  // Token = chained hash over normalized entries (stable order = append order)
  async function computeToken(entries){
    let h = '0'.repeat(64);
    for(const e of entries){
      const norm = JSON.stringify({
        segment: e.segment || '',
        title: e.title || '',
        body: e.body || '',
        created_local: e.created_local || ''
      });
      h = await sha256Hex(h + '|' + norm);
    }
    return h;
  }
  async function addEntry(entry){
    const entries = load();
    entries.push({
      segment: entry.segment || '',
      title: entry.title || '',
      body: entry.body || '',
      created_local: entry.created_local || new Date().toISOString()
    });
    save(entries);
    // store latest token for quick access (optional)
    try{
      const token = await computeToken(entries);
      localStorage.setItem('TT_CONTINUITY_TOKEN_V1', token);
    }catch(e){}
  }
  window.TTJournal = { load, addEntry, computeToken };
})();
