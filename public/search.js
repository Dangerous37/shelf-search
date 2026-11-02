const docs = [
  {id:'audit',topic:'Datos',title:'Auditoría de importaciones',body:'Reconcile source records and review import exceptions.'},
  {id:'restore',topic:'Datos',title:'Restore a snapshot',body:'Comprueba el inventario y registra la auditoría de restauración.'},
  {id:'slots',topic:'Reservas',title:'Confirmar una reserva',body:'Check availability before confirming a booking.'}
];
const byId = id => document.getElementById(id);
const fold = text => text.normalize('NFD').replace(/\p{M}/gu,'').toLowerCase();
const q = byId('q'), topic = byId('topic');
const initial = new URLSearchParams(location.search);
q.value = initial.get('q') || '';
topic.value = initial.get('topic') || '';
function render() {
  const terms = fold(q.value.trim()).split(/\s+/).filter(Boolean);
  const ranked = docs.map(doc => {
    const title = fold(doc.title), body = fold(doc.body);
    const scores = terms.map(t => title.includes(t) ? 3 : body.includes(t) ? 1 : 0);
    return {doc, match: scores.every(Boolean), score: scores.reduce((a,b)=>a+b,0)};
  }).filter(x => x.match && (!topic.value || topic.value === x.doc.topic))
    .sort((a,b)=>b.score-a.score || a.doc.title.localeCompare(b.doc.title,'es'));
  byId('results').replaceChildren();
  for (const {doc} of ranked) {
    const link = document.createElement('a'), item = document.createElement('li');
    link.href = '#' + doc.id;
    link.textContent = doc.title;
    item.append(link);
    byId('results').append(item);
  }
  byId('count').textContent = ranked.length + ' resultados';
  const url = new URL(location.href);
  for (const [key,value] of [['q',q.value],['topic',topic.value]]) {
    if (value) url.searchParams.set(key,value); else url.searchParams.delete(key);
  }
  history.replaceState(null,'',url);
  const selected = ranked.find(({doc}) => '#' + doc.id === location.hash);
  byId('detail').textContent = selected ? selected.doc.body : '';
}
q.addEventListener('input',render);
topic.addEventListener('change',render);
window.addEventListener('hashchange',render);
render();
