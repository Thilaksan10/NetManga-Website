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

var withdraw_card = document.querySelector('.card-body-withdraw')
if(withdraw_card){
    document.querySelector('.card-body-withdraw').addEventListener('click',function(){
        document.querySelector('.bg-modal').style.display = 'flex';
    });
}

var mangaseries_tab = document.getElementById('mangaseries-tab')
var oneshot_tab = document.getElementById('oneshot-tab')
var mangaseries_view = document.getElementById('mangaseries')
var oneshot_view = document.getElementById('oneshot')

if(mangaseries_tab && oneshot_tab){
    mangaseries_tab.addEventListener('click',function(){
        mangaseries_tab.className = "nav-link active"
        mangaseries_view.className = "tab-pane fade show active"
        oneshot_tab.className = "nav-link"
        oneshot_view.className = "tab-pane fade"
    });
    oneshot_tab.addEventListener('click',function(){
        mangaseries_tab.className = "nav-link"
        mangaseries_view.className = "tab-pane fade"
        oneshot_tab.className = "nav-link active"
        oneshot_view.className = "tab-pane fade show active"
    });
}

var drama_mangaseries_tab = document.getElementById('drama-mangaseries-tab')
var drama_oneshot_tab = document.getElementById('drama-oneshot-tab')
var drama_mangaseries_view = document.getElementById('drama-mangaseries')
var drama_oneshot_view = document.getElementById('drama-oneshot')

if(drama_mangaseries_tab && drama_oneshot_tab){
    drama_mangaseries_tab.addEventListener('click',function(){
        drama_mangaseries_tab.className = "nav-link active"
        drama_mangaseries_view.className = "tab-pane fade show active"
        drama_oneshot_tab.className = "nav-link"
        drama_oneshot_view.className = "tab-pane fade"
    });
    drama_oneshot_tab.addEventListener('click',function(){
        drama_mangaseries_tab.className = "nav-link"
        drama_mangaseries_view.className = "tab-pane fade"
        drama_oneshot_tab.className = "nav-link active"
        drama_oneshot_view.className = "tab-pane fade show active"
    });
}

var comedy_mangaseries_tab = document.getElementById('comedy-mangaseries-tab')
var comedy_oneshot_tab = document.getElementById('comedy-oneshot-tab')
var comedy_mangaseries_view = document.getElementById('comedy-mangaseries')
var comedy_oneshot_view = document.getElementById('comedy-oneshot')

if(comedy_mangaseries_tab && comedy_oneshot_tab){
    comedy_mangaseries_tab.addEventListener('click',function(){
        comedy_mangaseries_tab.className = "nav-link active"
        comedy_mangaseries_view.className = "tab-pane fade show active"
        comedy_oneshot_tab.className = "nav-link"
        comedy_oneshot_view.className = "tab-pane fade"
    });
    comedy_oneshot_tab.addEventListener('click',function(){
        comedy_mangaseries_tab.className = "nav-link"
        comedy_mangaseries_view.className = "tab-pane fade"
        comedy_oneshot_tab.className = "nav-link active"
        comedy_oneshot_view.className = "tab-pane fade show active"
    });
}

var fantasy_mangaseries_tab = document.getElementById('fantasy-mangaseries-tab')
var fantasy_oneshot_tab = document.getElementById('fantasy-oneshot-tab')
var fantasy_mangaseries_view = document.getElementById('fantasy-mangaseries')
var fantasy_oneshot_view = document.getElementById('fantasy-oneshot')

if(fantasy_mangaseries_tab && fantasy_oneshot_tab){
    fantasy_mangaseries_tab.addEventListener('click',function(){
        fantasy_mangaseries_tab.className = "nav-link active"
        fantasy_mangaseries_view.className = "tab-pane fade show active"
        fantasy_oneshot_tab.className = "nav-link"
        fantasy_oneshot_view.className = "tab-pane fade"
    });
    fantasy_oneshot_tab.addEventListener('click',function(){
        fantasy_mangaseries_tab.className = "nav-link"
        fantasy_mangaseries_view.className = "tab-pane fade"
        fantasy_oneshot_tab.className = "nav-link active"
        fantasy_oneshot_view.className = "tab-pane fade show active"
    });
}

var slice_of_life_mangaseries_tab = document.getElementById('slice-of-life-mangaseries-tab')
var slice_of_life_oneshot_tab = document.getElementById('slice-of-life-oneshot-tab')
var slice_of_life_mangaseries_view = document.getElementById('slice-of-life-mangaseries')
var slice_of_life_oneshot_view = document.getElementById('slice-of-life-oneshot')

if(slice_of_life_mangaseries_tab && slice_of_life_oneshot_tab){
    slice_of_life_mangaseries_tab.addEventListener('click',function(){
        slice_of_life_mangaseries_tab.className = "nav-link active"
        slice_of_life_mangaseries_view.className = "tab-pane fade show active"
        slice_of_life_oneshot_tab.className = "nav-link"
        slice_of_life_oneshot_view.className = "tab-pane fade"
    });
    slice_of_life_oneshot_tab.addEventListener('click',function(){
        slice_of_life_mangaseries_tab.className = "nav-link"
        slice_of_life_mangaseries_view.className = "tab-pane fade"
        slice_of_life_oneshot_tab.className = "nav-link active"
        slice_of_life_oneshot_view.className = "tab-pane fade show active"
    });
}

var romance_mangaseries_tab = document.getElementById('romance-mangaseries-tab')
var romance_oneshot_tab = document.getElementById('romance-oneshot-tab')
var romance_mangaseries_view = document.getElementById('romance-mangaseries')
var romance_oneshot_view = document.getElementById('romance-oneshot')

if(romance_mangaseries_tab && romance_oneshot_tab){
    romance_mangaseries_tab.addEventListener('click',function(){
        romance_mangaseries_tab.className = "nav-link active"
        romance_mangaseries_view.className = "tab-pane fade show active"
        romance_oneshot_tab.className = "nav-link"
        romance_oneshot_view.className = "tab-pane fade"
    });
    romance_oneshot_tab.addEventListener('click',function(){
        romance_mangaseries_tab.className = "nav-link"
        romance_mangaseries_view.className = "tab-pane fade"
        romance_oneshot_tab.className = "nav-link active"
        romance_oneshot_view.className = "tab-pane fade show active"
    });
}

var superhero_mangaseries_tab = document.getElementById('superhero-mangaseries-tab')
var superhero_oneshot_tab = document.getElementById('superhero-oneshot-tab')
var superhero_mangaseries_view = document.getElementById('superhero-mangaseries')
var superhero_oneshot_view = document.getElementById('superhero-oneshot')

if(superhero_mangaseries_tab && superhero_oneshot_tab){
    superhero_mangaseries_tab.addEventListener('click',function(){
        superhero_mangaseries_tab.className = "nav-link active"
        superhero_mangaseries_view.className = "tab-pane fade show active"
        superhero_oneshot_tab.className = "nav-link"
        superhero_oneshot_view.className = "tab-pane fade"
    });
    superhero_oneshot_tab.addEventListener('click',function(){
        superhero_mangaseries_tab.className = "nav-link"
        superhero_mangaseries_view.className = "tab-pane fade"
        superhero_oneshot_tab.className = "nav-link active"
        superhero_oneshot_view.className = "tab-pane fade show active"
    });
}

var sci_fi_mangaseries_tab = document.getElementById('sci-fi-mangaseries-tab')
var sci_fi_oneshot_tab = document.getElementById('sci-fi-oneshot-tab')
var sci_fi_mangaseries_view = document.getElementById('sci-fi-mangaseries')
var sci_fi_oneshot_view = document.getElementById('sci-fi-oneshot')

if(sci_fi_mangaseries_tab && sci_fi_oneshot_tab){
    sci_fi_mangaseries_tab.addEventListener('click',function(){
        sci_fi_mangaseries_tab.className = "nav-link active"
        sci_fi_mangaseries_view.className = "tab-pane fade show active"
        sci_fi_oneshot_tab.className = "nav-link"
        sci_fi_oneshot_view.className = "tab-pane fade"
    });
    sci_fi_oneshot_tab.addEventListener('click',function(){
        sci_fi_mangaseries_tab.className = "nav-link"
        sci_fi_mangaseries_view.className = "tab-pane fade"
        sci_fi_oneshot_tab.className = "nav-link active"
        sci_fi_oneshot_view.className = "tab-pane fade show active"
    });
}

var thriller_mangaseries_tab = document.getElementById('thriller-mangaseries-tab')
var thriller_oneshot_tab = document.getElementById('thriller-oneshot-tab')
var thriller_mangaseries_view = document.getElementById('thriller-mangaseries')
var thriller_oneshot_view = document.getElementById('thriller-oneshot')

if(thriller_mangaseries_tab && thriller_oneshot_tab){
    thriller_mangaseries_tab.addEventListener('click',function(){
        thriller_mangaseries_tab.className = "nav-link active"
        thriller_mangaseries_view.className = "tab-pane fade show active"
        thriller_oneshot_tab.className = "nav-link"
        thriller_oneshot_view.className = "tab-pane fade"
    });
    thriller_oneshot_tab.addEventListener('click',function(){
        thriller_mangaseries_tab.className = "nav-link"
        thriller_mangaseries_view.className = "tab-pane fade"
        thriller_oneshot_tab.className = "nav-link active"
        thriller_oneshot_view.className = "tab-pane fade show active"
    });
}

var supernatural_mangaseries_tab = document.getElementById('supernatural-mangaseries-tab')
var supernatural_oneshot_tab = document.getElementById('supernatural-oneshot-tab')
var supernatural_mangaseries_view = document.getElementById('supernatural-mangaseries')
var supernatural_oneshot_view = document.getElementById('supernatural-oneshot')

if(supernatural_mangaseries_tab && supernatural_oneshot_tab){
    supernatural_mangaseries_tab.addEventListener('click',function(){
        supernatural_mangaseries_tab.className = "nav-link active"
        supernatural_mangaseries_view.className = "tab-pane fade show active"
        supernatural_oneshot_tab.className = "nav-link"
        supernatural_oneshot_view.className = "tab-pane fade"
    });
    supernatural_oneshot_tab.addEventListener('click',function(){
        supernatural_mangaseries_tab.className = "nav-link"
        supernatural_mangaseries_view.className = "tab-pane fade"
        supernatural_oneshot_tab.className = "nav-link active"
        supernatural_oneshot_view.className = "tab-pane fade show active"
    });
}

var mystery_mangaseries_tab = document.getElementById('mystery-mangaseries-tab')
var mystery_oneshot_tab = document.getElementById('mystery-oneshot-tab')
var mystery_mangaseries_view = document.getElementById('mystery-mangaseries')
var mystery_oneshot_view = document.getElementById('mystery-oneshot')

if(mystery_mangaseries_tab && mystery_oneshot_tab){
    mystery_mangaseries_tab.addEventListener('click',function(){
        mystery_mangaseries_tab.className = "nav-link active"
        mystery_mangaseries_view.className = "tab-pane fade show active"
        mystery_oneshot_tab.className = "nav-link"
        mystery_oneshot_view.className = "tab-pane fade"
    });
    mystery_oneshot_tab.addEventListener('click',function(){
        mystery_mangaseries_tab.className = "nav-link"
        mystery_mangaseries_view.className = "tab-pane fade"
        mystery_oneshot_tab.className = "nav-link active"
        mystery_oneshot_view.className = "tab-pane fade show active"
    });
}

var sports_mangaseries_tab = document.getElementById('sports-mangaseries-tab')
var sports_oneshot_tab = document.getElementById('sports-oneshot-tab')
var sports_mangaseries_view = document.getElementById('sports-mangaseries')
var sports_oneshot_view = document.getElementById('sports-oneshot')

if(sports_mangaseries_tab && sports_oneshot_tab){
    sports_mangaseries_tab.addEventListener('click',function(){
        sports_mangaseries_tab.className = "nav-link active"
        sports_mangaseries_view.className = "tab-pane fade show active"
        sports_oneshot_tab.className = "nav-link"
        sports_oneshot_view.className = "tab-pane fade"
    });
    sports_oneshot_tab.addEventListener('click',function(){
        sports_mangaseries_tab.className = "nav-link"
        sports_mangaseries_view.className = "tab-pane fade"
        sports_oneshot_tab.className = "nav-link active"
        sports_oneshot_view.className = "tab-pane fade show active"
    });
}

var historical_mangaseries_tab = document.getElementById('historical-mangaseries-tab')
var historical_oneshot_tab = document.getElementById('historical-oneshot-tab')
var historical_mangaseries_view = document.getElementById('historical-mangaseries')
var historical_oneshot_view = document.getElementById('historical-oneshot')

if(historical_mangaseries_tab && historical_oneshot_tab){
    historical_mangaseries_tab.addEventListener('click',function(){
        historical_mangaseries_tab.className = "nav-link active"
        historical_mangaseries_view.className = "tab-pane fade show active"
        historical_oneshot_tab.className = "nav-link"
        historical_oneshot_view.className = "tab-pane fade"
    });
    historical_oneshot_tab.addEventListener('click',function(){
        historical_mangaseries_tab.className = "nav-link"
        historical_mangaseries_view.className = "tab-pane fade"
        historical_oneshot_tab.className = "nav-link active"
        historical_oneshot_view.className = "tab-pane fade show active"
    });
}

var heartwarming_mangaseries_tab = document.getElementById('heartwarming-mangaseries-tab')
var heartwarming_oneshot_tab = document.getElementById('heartwarming-oneshot-tab')
var heartwarming_mangaseries_view = document.getElementById('heartwarming-mangaseries')
var heartwarming_oneshot_view = document.getElementById('heartwarming-oneshot')

if(heartwarming_mangaseries_tab && heartwarming_oneshot_tab){
    heartwarming_mangaseries_tab.addEventListener('click',function(){
        heartwarming_mangaseries_tab.className = "nav-link active"
        heartwarming_mangaseries_view.className = "tab-pane fade show active"
        heartwarming_oneshot_tab.className = "nav-link"
        heartwarming_oneshot_view.className = "tab-pane fade"
    });
    heartwarming_oneshot_tab.addEventListener('click',function(){
        heartwarming_mangaseries_tab.className = "nav-link"
        heartwarming_mangaseries_view.className = "tab-pane fade"
        heartwarming_oneshot_tab.className = "nav-link active"
        heartwarming_oneshot_view.className = "tab-pane fade show active"
    });
}

var horror_mangaseries_tab = document.getElementById('horror-mangaseries-tab')
var horror_oneshot_tab = document.getElementById('horror-oneshot-tab')
var horror_mangaseries_view = document.getElementById('horror-mangaseries')
var horror_oneshot_view = document.getElementById('horror-oneshot')

if(horror_mangaseries_tab && horror_oneshot_tab){
    horror_mangaseries_tab.addEventListener('click',function(){
        horror_mangaseries_tab.className = "nav-link active"
        horror_mangaseries_view.className = "tab-pane fade show active"
        horror_oneshot_tab.className = "nav-link"
        horror_oneshot_view.className = "tab-pane fade"
    });
    horror_oneshot_tab.addEventListener('click',function(){
        horror_mangaseries_tab.className = "nav-link"
        horror_mangaseries_view.className = "tab-pane fade"
        horror_oneshot_tab.className = "nav-link active"
        horror_oneshot_view.className = "tab-pane fade show active"
    });
}

var informative_mangaseries_tab = document.getElementById('informative-mangaseries-tab')
var informative_oneshot_tab = document.getElementById('informative-oneshot-tab')
var informative_mangaseries_view = document.getElementById('informative-mangaseries')
var informative_oneshot_view = document.getElementById('informative-oneshot')

if(informative_mangaseries_tab && informative_oneshot_tab){
    informative_mangaseries_tab.addEventListener('click',function(){
        informative_mangaseries_tab.className = "nav-link active"
        informative_mangaseries_view.className = "tab-pane fade show active"
        informative_oneshot_tab.className = "nav-link"
        informative_oneshot_view.className = "tab-pane fade"
    });
    informative_oneshot_tab.addEventListener('click',function(){
        informative_mangaseries_tab.className = "nav-link"
        informative_mangaseries_view.className = "tab-pane fade"
        informative_oneshot_tab.className = "nav-link active"
        informative_oneshot_view.className = "tab-pane fade show active"
    });
}

var action_mangaseries_tab = document.getElementById('action-mangaseries-tab')
var action_oneshot_tab = document.getElementById('action-oneshot-tab')
var action_mangaseries_view = document.getElementById('action-mangaseries')
var action_oneshot_view = document.getElementById('action-oneshot')

if(action_mangaseries_tab && action_oneshot_tab){
    action_mangaseries_tab.addEventListener('click',function(){
        action_mangaseries_tab.className = "nav-link active"
        action_mangaseries_view.className = "tab-pane fade show active"
        action_oneshot_tab.className = "nav-link"
        action_oneshot_view.className = "tab-pane fade"
    });
    action_oneshot_tab.addEventListener('click',function(){
        action_mangaseries_tab.className = "nav-link"
        action_mangaseries_view.className = "tab-pane fade"
        action_oneshot_tab.className = "nav-link active"
        action_oneshot_view.className = "tab-pane fade show active"
    });
}

var pending_tab = document.getElementById('pending-tab')
var failed_tab = document.getElementById('failed-tab')
var succeeded_tab = document.getElementById('succeeded-tab')
var pending_view = document.getElementById('pending')
var failed_view = document.getElementById('failed')
var succeeded_view = document.getElementById('succeeded')

if(pending_tab && failed_tab && succeeded_tab){
    pending_tab.addEventListener('click',function(){
        pending_tab.className = "nav-link active"
        pending_view.className = "tab-pane fade show active"
        failed_tab.className = "nav-link"
        failed_view.className = "tab-pane fade"
        succeeded_tab.className = "nav-link"
        succeeded_view.className = "tab-pane fade"
    });
    failed_tab.addEventListener('click',function(){
        pending_tab.className = "nav-link"
        pending_view.className = "tab-pane fade"
        failed_tab.className = "nav-link active"
        failed_view.className = "tab-pane fade show active"
        succeeded_tab.className = "nav-link"
        succeeded_view.className = "tab-pane fade"
    });
    succeeded_tab.addEventListener('click',function(){
        pending_tab.className = "nav-link"
        pending_view.className = "tab-pane fade"
        failed_tab.className = "nav-link"
        failed_view.className = "tab-pane fade"
        succeeded_tab.className = "nav-link active"
        succeeded_view.className = "tab-pane fade show active"
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

var before2 = document.querySelector('#mangaPagesBrowseButton > .before') 
var after2 = document.querySelector('#mangaPagesBrowseButton > .after')
var manga_pages = document.querySelector("#id_manga_pages");
if(manga_pages && (before2 || after2)){
    manga_pages.addEventListener("change", function() {
        if(this.files.length <= 200 ){
            var total_size = 0
            for(i=0; i<this.files.length; i++){
                total_size += this.files[i].size
                console.log(total_size/1000000 + "MB")
            }
            if(total_size <= 50000000){
                if(before2){
                    before2.className = "after"
                }
                
                images = document.getElementsByClassName("uploaded-manga-pages")
                console.log(images)
                while(images[0]){
                    console.log(images[0])
                    images[0].parentNode.removeChild(images[0])
                }
                for(i=0; i<this.files.length; i++){
                    var img = document.createElement('img');
                    img.src = URL.createObjectURL(this.files[i])
                    img.className = "uploaded-manga-pages"
                    if(before2){
                        before2.appendChild(img)
                    }
                    else{
                        after2.appendChild(img)
                    }
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

if(document.querySelector(".page-card")){
    document.querySelector(".page-card").addEventListener("touchstart", startTouch, false);
    document.querySelector(".page-card").addEventListener("touchmove", moveTouch, false);

    var initialX = null;
    var initialY = null;
    
    function startTouch(e) {
        initialX = e.touches[0].clientX;
        initialY = e.touches[0].clientY;
    };
    
    function moveTouch(e) {
        if (initialX === null) {
            return;
        }
        
        if (initialY === null) {
            return;
        }
        
        var currentX = e.touches[0].clientX;
        var currentY = e.touches[0].clientY;
        
        var diffX = initialX - currentX;
        var diffY = initialY - currentY;
        
        if (Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX > 0) {
            // swiped left
            document.getElementById('previous-page').click();
            } else {
            // swiped right
            document.getElementById('next-page').click();
            } 
        } 
        
        
        initialX = null;
        
        e.preventDefault();
    }
}

