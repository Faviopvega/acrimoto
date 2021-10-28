const btndelete = document.querySelectorAll('.btn-delete')

if (btndelete){
    const btnArray = Array.from(btndelete);
    btnArray.forEach((btn)=>{
        btn.addEventListener('click', (e) =>{

            if(!confirm('Realmente Desea Eliminar el Registro?')){
                e.preventDefault()
            }
        });
    });
}
