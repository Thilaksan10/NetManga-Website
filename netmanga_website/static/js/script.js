var payment_close = document.querySelector('.payment-close')
if(payment_close){
    document.querySelector('.payment-close').addEventListener('click',function(){
        document.querySelector('.bg-payment-modal').style.display='none';
        document.documentElement.style.overflow='scroll';
        document.body.scroll = "yes";
    });
}

var edit_profile = document.getElementById('edit-profile')
if(edit_profile){
    document.getElementById('edit-profile').addEventListener('click',function(){
        document.querySelector('.bg-modal').style.display = 'flex';
    });
}

var close = document.querySelector('.close')
if(close){
    document.querySelector('.close').addEventListener('click',function(){
        document.querySelector('.bg-modal').style.display = 'none';
    });
}

var manga_page = document.getElementById('manga-page')
if(manga_page){
    document.getElementById('manga-page').setAttribute('draggable',false);
}

var give_award = document.getElementById('give_award')
if(give_award){
    document.getElementById('give_award').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display = 'flex';
    });
}

var awards_close = document.querySelector('.awards-close')
if(awards_close){
    document.querySelector('.awards-close').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display='none';
    });
}

var coins_amount = document.querySelector('.coins-amount-view')
if(coins_amount){
    document.querySelector('.coins-amount-view').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display='none';
        document.querySelector('.bg-reloadpage-modal').style.display='flex';
    });
}

var give_bronce_award = document.getElementById('label_bronceaward_link')
if(give_bronce_award){
    document.getElementById('label_bronceaward_link').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display='none';
        document.querySelector('.bg-reloadpage-modal').style.display='flex';
    });
}

var give_silver_award = document.getElementById('label_silveraward_link')
if(give_silver_award){
    document.getElementById('label_silveraward_link').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display='none';
        document.querySelector('.bg-reloadpage-modal').style.display='flex';
    });
}

var give_gold_award = document.getElementById('label_goldaward_link')
if(give_gold_award){
    document.getElementById('label_goldaward_link').addEventListener('click',function(){
        document.querySelector('.bg-awards-modal').style.display='none';
        document.querySelector('.bg-reloadpage-modal').style.display='flex';
    });
}

var report_chapter = document.getElementById('report_chapter')
if(report_chapter){
    document.getElementById('report_chapter').addEventListener('click',function(){
        document.querySelector('.bg-report-modal').style.display = 'flex';
    });
}

var report_close = document.querySelector('.report-close')
if(report_close){
    document.querySelector('.report-close').addEventListener('click',function(){
        document.querySelector('.bg-report-modal').style.display='none';
    });
} 