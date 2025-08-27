
var responsiveSlider = function(){
	
	var slider = document.getElementById("slider");
	var sliderWidth = slider.offsetWidth;
	var slideList = document.getElementById("sliderWrap");
	var items = slideList.querySelectorAll("li").length;
	
	var count = 0;
	
	var num = document.getElementById("num");
	slideNums = num.querySelectorAll("div");
	
	var prev = document.getElementById("prev");
	var next = document.getElementById("next");
	
	var addColor = function(pos){
		slideNums[pos].style.boxShadow = "0 0 10px 2px rgb(196, 253, 255)";
		slideNums[pos].style.background = "#fff";
	}
	
	var removeColor = function(pos){
		slideNums[pos].style.boxShadow = "0 0 10px 2px transparent";
		slideNums[pos].style.background = "rgba(255, 255, 255, .3)";
	}
	
	addColor(0);
	
	slideNums[0].addEventListener("click", function(){
		removeColor(count);
		count = 0;
		addColor(count);
		slideList.style.left = "0px";
	});
	slideNums[1].addEventListener("click", function(){
		removeColor(count);
		count = 1;
		addColor(count);
		slideList.style.left = "-" + count * sliderWidth + "px";
	});
	slideNums[2].addEventListener("click", function(){
		removeColor(count);
		count = 2;
		addColor(count);
		slideList.style.left = "-" + count * sliderWidth + "px";
	});
	
	
	window.addEventListener("resize", function(){
		sliderWidth = slider.offsetWidth;
		slideList.style.left = "-" + count * sliderWidth + "px";
	});
	
	var prevSlide = function(){
		removeColor(count);
		if(!count) count = items - 1;
		else count--;
		addColor(count);
		slideList.style.left = "-" + count * sliderWidth + "px";
	}
	
	var nextSlide = function(){
		removeColor(count);
		if(count == items - 1) count = 0;
		else count++;
		addColor(count);
		slideList.style.left =  "-" + count * sliderWidth + "px";
	}
	
	next.addEventListener("click", function(){
		nextSlide();
	}); 
	
	prev.addEventListener("click", function(){
		prevSlide();
	});
	
	setInterval(function(){
		nextSlide();
	}, 8000);
}

window.onload = function(){
	responsiveSlider();
}


