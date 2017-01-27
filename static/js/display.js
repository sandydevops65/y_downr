var cleanUp = function(){
    var url = document.getElementById("url");
    url.value = "";
    url.focus();
};

document.onload = cleanUp;
document.onbeforeunload = cleanUp;
var d;
var build_atomic = function(res){
    var result = document.getElementById("result");
    var h4 = document.createElement("h4");
    h4.textContent = res.title;
    result.appendChild(h4)
    var info = res.info;
    var p2 = document.createElement("p");
    for (var j=0; j<info.length; j++){
        var a = document.createElement("a");
        a.textContent = info[j][1]+": "+info[j][0];
        a.classList.add("button");
        a.href = info[j][2]
        p2.appendChild(a);
    }
    result.appendChild(p2);
    
};

var emptyNode = function(id){
    var node = document.getElementById(id);
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
};

var createOne = function(id){
    var h4 = document.createElement("h4");
    h4.textContent = id.split("$").join(" ");
    var el = document.createElement("textarea");
    el.readOnly = true;
    el.id = id;
    el.classList.add("u-full-width");
    el.setAttribute("onfocus", "this.select()");
    var div = document.createElement("div");
    div.classList.add("each");
    div.appendChild(h4);
    div.appendChild(el);
    var tabbed = document.getElementById("tabbed");
    tabbed.appendChild(div);
    return el;
};

var build_list = function(res_){
    for (var i = 0; i < res_.length; i++) {
        var res = res_[i];
        var info = res.info
        for (var j=0; j<info.length; j++){
            var id = info[j][1]+"$"+info[j][0];
            var el = document.getElementById(id);
            var ta = (el)? el : createOne(id);
            ta.value += info[j][2] + "\n";
        }
        if (!document.getElementById("icon").checked && res.title && res.info.length){
            res.title = (i+1) + " : " + res.title;
            build_atomic(res); 
        }
    }
};

var build_display = function(res, kind){
    if(kind == "atom"){
        build_atomic(res);
    }else if(kind == "list"){
        build_list(res);
    }
    var url = document.getElementById("url");
    url.readOnly = false;
    url.select();
    url.focus();
    document.getElementById("submit").disabled = false;
}

var request = function(url, kind){
    var xhr = new XMLHttpRequest();
    var url = url;
    var kind = kind;
    console.log(kind);
    var data = "url="+encodeURIComponent(url) + "&kind=" + encodeURIComponent(kind);
    xhr.open("POST", "/creep");
    xhr.onreadystatechange = function(){
        if (xhr.status == 200 && xhr.readyState == 4){
            var res = JSON.parse(xhr.responseText);
            console.log(res);
            build_display(res, kind);
            d1 = new Date();
            console.log(d1);
            console.log(d1.getSeconds() - d.getSeconds());
        }
    };
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);
};


document.getElementById('submit').onclick = function (e) {
    var valid = false;
    var kind;
    var url = document.getElementById("url");
    if (url.value.contains("/playlist?list=")){
        kind = "list";
        valid = true;
    }else if (url.value.contains("/watch?v=")){
        kind = "atom";
        valid = true;
    }else {
        console.log(url.value+": very dirty");
        url.style.borderColor = "red";
        url.select();
        url.focus();
        valid = false;
    }
    if (valid) {
        d = new Date();
        console.log(d);
        emptyNode("tabbed");
        emptyNode("result");
        url.readOnly = true;
        this.disabled = true;
        request(url.value, kind);
    }
};

document.getElementById("url").onkeydown = function(e){
    if (this.value == ""){
        url.style.borderColor = "";
    }
    if (e.keyCode == 13) {
        document.getElementById("submit").click();
    }
};

document.getElementById("url").onfocus = function(e){
    this.select();
};
