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

var withdraw_card =  document.querySelector('.card-body-withdraw')
if(withdraw_card){
    document.querySelector('.card-body-withdraw').addEventListener('click',function(){
        document.querySelector('.bg-modal').style.display = 'flex';
    });
}

function hover(element1, element2, className){
    element1.addEventListener('mouseenter', e => element2.classList.add(className))
    element1.addEventListener('mouseleave', e => element2.classList.remove(className))
  }

var coverPictureBrowseButton = document.getElementById('coverPictureBrowseButton')
var coverPicture = document.getElementById('id_cover_picture')
if(coverPictureBrowseButton && coverPicture){
    hover(coverPicture, coverPictureBrowseButton, "browse-over")
}

var profilePictureBrowseButton = document.getElementById('profilePictureBrowseButton')
var profilePicture = document.getElementById('id_profile_Picture')
if(profilePictureBrowseButton && profilePicture){
    hover(profilePicture, profilePictureBrowseButton, "browse-over")
}

var mangaPagesBrowseButton = document.getElementById('mangaPagesBrowseButton')
var manga_pages = document.getElementById('id_manga_pages')
if(mangaPagesBrowseButton && manga_pages){
    hover(manga_pages, mangaPagesBrowseButton, "mangapages-browse-over")
}

var image_input = document.querySelector("#id_cover_picture");
if(!image_input){
    
    var image_input = document.querySelector("#id_profile_Picture");

}
var before = document.querySelector('.before') 
var after = document.querySelector('.after')
if(image_input && (before || after)){
    image_input.addEventListener("change", function() {
        if(before){
            before.className = "after"
        }
        if(document.querySelector("#coverpicturepreview")){
            document.querySelector("#coverpicturepreview").src = URL.createObjectURL(this.files[0]);
        }
        else{
            document.querySelector("#profilepicturepreview").src = URL.createObjectURL(this.files[0]);
        }
    });
}


var manga_pages = document.querySelector("#id_manga_pages");
if(manga_pages && (before || after)){
    manga_pages.addEventListener("change", function() {
        if(this.files.length <= 200 ){
            var total_size = 0
            for(i=0; i<this.files.length; i++){
                total_size += this.files[i].size
                console.log(total_size/1000000 + "MB")
            }
            if(total_size <= 50000000){
                if(before){
                    before.className = "after"
                }
            
                images = document.getElementsByClassName("uploaded-manga-pages")
                while(images[0]){
                    images[0].parentNode.removeChild(images[0])
                }
                for(i=0; i<this.files.length; i++){
                    var img = document.createElement('img');
                    img.src = URL.createObjectURL(this.files[i])
                    img.className = "uploaded-manga-pages"
                    before.appendChild(img)
                    total_size += this.files[i].size  
                }
            }
            else{
                console.log("Uploaded files size is " + (total_size/1000000) + "MB. Total files size exeeds 50MB. ")
                if(document.getElementById("file-size-alert")){
                    console.log(document.querySelector("#file-size-alert .alert-text"));
                    document.querySelector("#file-size-alert .alert-text").innerHTML = "Uploaded files size is " + (total_size/1000000) + "MB. Total files size exeeds 50MB."
                    document.getElementById("file-size-alert").style.display = "block";
                }
            }
        }
        else {
            console.log('You can only upload up to 300 images.')
            if(document.getElementById("image-count-alert")){
                console.log(document.querySelector("#image-count-alert .alert-text"));
                document.querySelector("#image-count-alert .alert-text").innerHTML = "You uploaded " + this.files.length + " images, but you can only upload up to 300 images."
                document.getElementById("image-count-alert").style.display = "block";
            }
        }
    });
}

function sticky( element ){
    element.parentElement.parentElement.addEventListener("scroll", function(){
        element.style.transform = "translateY("+this.scrollTop+"px)";
    });
}

var manga_pages_box = document.querySelector(".manga-pages-box");
if(manga_pages_box){
    sticky(manga_pages_box);
}
