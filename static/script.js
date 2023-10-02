const navlinks=document.querySelectorAll('.nav-link');
const activePage=window.location.pathname;

navlinks.forEach(link => {
    const navlinkpath=new URL(link.href).pathname;
    if(navlinkpath==activePage){
        
        link.classList.add('active');
        
    }
    
});
