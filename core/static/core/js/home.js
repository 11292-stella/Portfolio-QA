/* Simulazioni "form che si compila da solo" della home.
   I dati arrivano dal database tramite i tag <script type="application/json"> (json_script) del template. */

/* Helper condivisi da tutte le simulazioni della pagina */
window.__sim = (function () {
    /* "Salta animazioni": se attivo (o se l'utente preferisce meno animazioni)
       i form si compilano all'istante e i cicli si fermano sul primo elemento. */
    let skipped = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    const isSkipped = () => skipped;
    const skip = () => { skipped = true; };
    const sleep = ms => skipped ? Promise.resolve() : new Promise(r => setTimeout(r, ms));

    async function typeText(node, text, speed = 14) {
        if (skipped) { node.classList.add('active'); node.textContent = text; return; }
        node.classList.add('active');
        node.innerHTML = '<span class="typed"></span><span class="cursor-blink"></span>';
        const typed = node.querySelector('.typed');
        for (const ch of text) { typed.textContent += ch; await sleep(speed); }
        await sleep(300);
        node.querySelector('.cursor-blink')?.remove();
    }

    async function selectFake(node, label) {
        node.classList.add('active');
        node.textContent = '';
        await sleep(150);
        node.textContent = label;
        await sleep(400);
    }

    async function fillUpload(node, delay = 1400) {
        node.classList.add('active');
        await sleep(delay);
    }

    function renderPills(container, list) {
        container.innerHTML = '';
        list.forEach(t => {
            const span = document.createElement('span');
            span.className = 'pill';
            span.textContent = t;
            span.dataset.tech = t;
            container.appendChild(span);
        });
    }

    async function checkPill(container, tech, delay = 220) {
        const pill = container.querySelector(`[data-tech="${CSS.escape(tech)}"]`);
        if (pill) { pill.classList.add('on'); await sleep(delay); }
    }

    async function checkAllPills(container, delay = 150) {
        const items = [...container.children];
        items.forEach(async (p, i) => { await sleep(i * delay); p.classList.add('on'); });
        await sleep(items.length * delay + 200);
    }

    async function runExperienceSim(prefix, DATASET, ALL_TECH) {
        const el = id => document.getElementById(prefix + '-' + id);
        const azione = el('azione'), area = el('area'), pills = el('pills'),
              techRow = el('tech-row'), dettaglio = el('dettaglio'), ordine = el('ordine'),
              btn = el('btn'), status = el('status');

        if (!ALL_TECH.length) { if (techRow) techRow.style.display = 'none'; }
        else { renderPills(pills, ALL_TECH); }

        async function resetForm() {
            azione.textContent = '- Seleziona -'; azione.classList.remove('active');
            area.textContent = '- Seleziona -'; area.classList.remove('active');
            dettaglio.innerHTML = ''; dettaglio.classList.remove('active');
            ordine.textContent = '0';
            if (ALL_TECH.length) renderPills(pills, ALL_TECH);
            btn.classList.remove('saved');
            status.innerHTML = '&nbsp;';
            await sleep(500);
        }

        async function cycle() {
            for (const item of DATASET) {
                await resetForm();
                await selectFake(azione, item.azione);
                await selectFake(area, item.area);
                if (item.tech) for (const t of item.tech) await checkPill(pills, t);
                await typeText(dettaglio, item.dettaglio, 16);
                ordine.textContent = String(item.ordine);
                await sleep(300);
                btn.classList.add('saved');
                status.innerHTML = '<span class="ok">&#10003;</span> highlight salvato';
                if (skipped) return;
                await sleep(1400);
            }
            await sleep(700);
            cycle();
        }
        cycle();
    }

    return { sleep, isSkipped, skip, typeText, selectFake, fillUpload, renderPills, checkPill, checkAllPills, runExperienceSim };
})();

(function () {
    const b = document.getElementById('skip-anim');
    if (window.__sim.isSkipped()) { b.hidden = true; return; }
    b.addEventListener('click', () => { window.__sim.skip(); b.hidden = true; });
})();

(function () {
    const S = window.__sim;
    const RUOLO = "QA Automation Engineer & Full Stack Developer";
    const DISP = "Full Remote / Disponibile a Trasferimento | Dipendente & Freelance (P.IVA)";
    const BIO = "Sono una QA Automation Engineer con un background da Full Stack Developer. Sviluppo e mantengo architetture di test automatici E2E e pipeline CI/CD (Cypress, Playwright, Appium, GitLab CI), garantendo la stabilità delle applicazioni dal codice alla sicurezza. La mia formazione nello sviluppo mi permette di leggere e analizzare direttamente il codice sorgente per individuare la radice dei problemi, mentre le mie origini nel graphic design guidano la mia attenzione per l'usabilità e la UX.";
    const OBIETTIVO = `Aperta a collaborazioni sia in Partita IVA sia come dipendente (Full Remote o con disponibilità al trasferimento). Cerco opportunità come QA Automation Engineer, Full Stack Developer o in ruoli ibridi, dove mettere a disposizione la progettazione autonoma di framework E2E multi-stack, il debug di codice frontend/backend e lo sviluppo software.`;
    // lo stack arriva dalle Skill nel database (stessa fonte della sezione skills)
    const skillsEl = document.getElementById('skills-data');
    const TECH = skillsEl ? Object.values(JSON.parse(skillsEl.textContent)).flat() : [];

    const el = id => document.getElementById(id);
    const ruolo = el('ps-ruolo'), disp = el('ps-disp'), foto = el('ps-foto'), bio = el('ps-bio'),
          obiettivo = el('ps-obiettivo'), pills = el('ps-pills'), btn = el('ps-btn'),
          status = el('ps-status');

    async function resetForm() {
        ruolo.textContent = '- Seleziona -'; ruolo.classList.remove('active');
        disp.textContent = '- Seleziona -'; disp.classList.remove('active');
        foto.classList.remove('active');
        bio.innerHTML = ''; bio.classList.remove('active');
        obiettivo.innerHTML = ''; obiettivo.classList.remove('active');
        S.renderPills(pills, TECH);
        btn.classList.remove('saved');
        status.innerHTML = '&nbsp;';
        await S.sleep(500);
    }

    async function runCycle() {
        {
            await resetForm();
            await S.selectFake(ruolo, RUOLO);
            await S.selectFake(disp, DISP);
            await S.fillUpload(foto);
            await S.typeText(bio, BIO);
            await S.typeText(obiettivo, OBIETTIVO);
            await S.checkAllPills(pills);
            await S.sleep(300);
            btn.classList.add('saved');
            status.innerHTML = '<span class="ok">&#10003;</span> presentazione salvata';
        }
    }

    S.renderPills(pills, TECH);
    runCycle();
})();

(function () {
    const dataEl = document.getElementById('sellogic-sim-data');
    if (!dataEl) return;
    const data = JSON.parse(dataEl.textContent);
    if (data.dataset.length) window.__sim.runExperienceSim('sg', data.dataset, data.all_tech);
})();

(function () {
    const dataEl = document.getElementById('iliad-sim-data');
    if (!dataEl) return;
    const data = JSON.parse(dataEl.textContent);
    if (data.dataset.length) window.__sim.runExperienceSim('il', data.dataset, data.all_tech);
})();

(function () {
    const S = window.__sim;
    const dataEl = document.getElementById('skills-data');
    if (!dataEl) return;
    const DATA = JSON.parse(dataEl.textContent);
    const CATS = Object.keys(DATA);
    const categoria = document.getElementById('sk-categoria'), pills = document.getElementById('sk-pills');

    async function cycle() {
        for (const cat of CATS) {
            categoria.classList.remove('active');
            categoria.textContent = '- Seleziona -';
            S.renderPills(pills, DATA[cat]);
            await S.sleep(400);
            await S.selectFake(categoria, cat);
            await S.checkAllPills(pills, 110);
            if (S.isSkipped()) return;
            await S.sleep(1200);
        }
        await S.sleep(500);
        cycle();
    }
    if (CATS.length) cycle();
})();

(function () {
    const S = window.__sim;
    const dataEl = document.getElementById('formazione-sim-data');
    if (!dataEl) return;
    const DATA = JSON.parse(dataEl.textContent);
    if (!DATA.length) return;
    const el = id => document.getElementById('fm-' + id);
    const istituto = el('istituto'), periodo = el('periodo'), titolo = el('titolo'),
          dettaglio = el('dettaglio'), pillsRow = el('tech-row'), pills = el('pills'),
          btn = el('btn'), status = el('status');

    async function resetForm(techList) {
        istituto.textContent = '- Seleziona -'; istituto.classList.remove('active');
        periodo.textContent = '- Seleziona -'; periodo.classList.remove('active');
        titolo.textContent = '- Seleziona -'; titolo.classList.remove('active');
        dettaglio.innerHTML = ''; dettaglio.classList.remove('active');
        if (techList.length) { pillsRow.style.display = ''; S.renderPills(pills, techList); }
        else { pillsRow.style.display = 'none'; }
        btn.classList.remove('saved');
        status.innerHTML = '&nbsp;';
        await S.sleep(500);
    }

    async function cycle() {
        for (const item of DATA) {
            await resetForm(item.tech || []);
            await S.selectFake(istituto, item.istituto);
            await S.selectFake(periodo, item.periodo);
            await S.selectFake(titolo, item.titolo);
            await S.typeText(dettaglio, item.dettaglio, 14);
            if (item.tech && item.tech.length) await S.checkAllPills(pills, 130);
            await S.sleep(300);
            btn.classList.add('saved');
            status.innerHTML = '<span class="ok">&#10003;</span> formazione salvata';
            if (S.isSkipped()) return;
            await S.sleep(1600);
        }
        await S.sleep(700);
        cycle();
    }
    cycle();
})();
