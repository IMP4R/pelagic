(()=>{
const portrait=matchMedia('(max-width:700px) and (orientation:portrait)');
const quote=document.querySelector('.quote h2'),original=quote.innerHTML;
function compose(){if(portrait.matches){quote.innerHTML='<span class="line"><span>NOT EMPTY.</span></span><span class="line"><span>UNSEEN.</span></span>'}else quote.innerHTML=original;const water=document.querySelector('#water-toggle'),menu=document.querySelector('#mobile-navigation');if(water&&menu){if(portrait.matches)menu.append(water);else document.body.append(water)}}compose();portrait.addEventListener('change',compose);
// Only one mobile beat earns a long hold; shorten the other two without changing desktop.
const css=document.createElement('style');css.textContent='@media(max-width:700px) and (orientation:portrait){.hero{height:165svh!important}#life{height:175svh!important}#abyss{height:185svh!important}}';document.head.append(css);
})();
