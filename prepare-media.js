// Download complete files before assigning video sources: first-frame readiness is not file readiness.
window.pelagicMedia=[...document.querySelectorAll('video[data-desktop]')].map((video,index)=>{
 const state={video,index,bytes:0,total:0,phase:'downloading',error:null,url:null};
 video.removeAttribute('autoplay');video.removeAttribute('loop');video.muted=true;video.defaultMuted=true;video.playsInline=true;video.preload='auto';
 const source=matchMedia('(pointer:coarse)').matches?video.dataset.mobile:video.dataset.desktop;
 video.style.backgroundImage=`url("${video.poster}")`;video.style.backgroundSize='cover';video.style.backgroundPosition='center';
 state.ready=(async()=>{try{
 const response=await fetch(source);if(!response.ok)throw Error('HTTP '+response.status);
 state.total=Number(response.headers.get('content-length'))||0;
 const reader=response.body?.getReader();let blob;
 if(reader){const parts=[];for(;;){const{done,value}=await reader.read();if(done)break;parts.push(value);state.bytes+=value.byteLength}blob=new Blob(parts,{type:'video/mp4'})}else{blob=await response.blob();state.bytes=blob.size}
 state.phase='decoding';state.url=URL.createObjectURL(blob);
 await new Promise((resolve,reject)=>{let timeout;function cleanup(){clearTimeout(timeout);video.removeEventListener('loadeddata',loaded);video.removeEventListener('error',failed)}function loaded(){if(video.readyState>=2){cleanup();resolve()}}function failed(){cleanup();reject(Error('Video decoding failed'))}video.addEventListener('loadeddata',loaded);video.addEventListener('error',failed);timeout=setTimeout(()=>{cleanup();reject(Error('Video decoding timeout'))},20000);video.src=state.url;video.load();loaded()});
 state.phase='ready';video.dataset.complete='yes';dispatchEvent(new Event('resize'));return state;
 }catch(error){state.phase='error';state.error=error.message;throw error}})();
 // Loader attaches its own failure handler later in this document.
 state.ready.catch(()=>{});return state;
});
