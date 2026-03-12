
(function(){
  const side = document.querySelector('.side');
  if(!side) return;
  const links = Array.from(side.querySelectorAll('a[data-target]'));
  const setActive = (id) => {
    links.forEach(a => a.classList.toggle('active', a.getAttribute('data-target')===id));
  };
  // If page has anchors, highlight based on scroll.
  const headings = Array.from(document.querySelectorAll('main .article h2[id], main .article h3[id]'));
  if(headings.length){
    const obs = new IntersectionObserver((entries)=>{
      const vis = entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if(!vis) return;
      const id = vis.target.id;
      // find first link that matches hash
      const match = links.find(a => a.getAttribute('href') === ('#'+id));
      if(match) setActive(match.getAttribute('data-target'));
    }, {rootMargin: "-25% 0px -65% 0px", threshold:[0.1,0.2,0.3,0.4,0.5]});
    headings.forEach(h=>obs.observe(h));
  }
})();
