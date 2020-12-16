// var socket =io('ws://127.0.0.1:8181');
var color = '';
var GRID_SIZE = 20;
var HORIZONTAL_SIZE = null;
var VERTICAL_SIZE = null;
var checkerBoard_type = new Array();
var checkerBoard_state = new Array();
var adjacentBlock = new Array();
//  # 0 is wait, 1 is vs_tree_ai, 2 is vs_human, 3 is vs_random, 4 is nn_vs_tree, 5 is vs_nn_ai,
// # 6 is nn vs nn, 7 is tree vs tree
var game_state = 0;

//for ai_vs_ai
var AI_next_x = '';
var AI_next_y = '';
var AI_next_color = 'black';

var cvs = document.getElementById('cvs');
var ctx = cvs.getContext('2d');


var uname = prompt('Please enter username', 'user' + uuid(8, 16));
var ws = new WebSocket("ws://127.0.0.1:1234");
ws.onopen = function () {
   var data = "Sys Msg: Build Connection";
   listMsg(data);
};

ws.onmessage = function(e) {
   var msg = JSON.parse(e.data);
   var sender, user_name, name_list, change_type,temp_color;

   switch (msg.type) {
      case 'system':
         sender = 'Sys Msg: ';
         break;
      case 'user':
         sender = msg.from + ': ';
         break;
      case 'handshake':
         var user_info = {
            'type': 'login',
            'content': uname
         };
         sendMsg(user_info);
         return;
      case 'login':
         user_name = msg.content;
         name_list = msg.user_list;
         change_type = msg.type;
         if(color==''){
            color = msg.color;
         }
         temp_color = msg.color;
         document.querySelector('#color').innerHTML = 'Hello '+uname+'. You are ' + color;
         if(color != 'visitor'){
            document.getElementById('set').disabled = false;
         }
         dealUser(user_name, change_type, name_list,temp_color);
        return;
      case 'logout':
         user_name = msg.content;
         name_list = msg.user_list;
         change_type = msg.type;
         temp_color = msg.color;

         dealUser(user_name, change_type, name_list, temp_color);
         return;
      case 'init':
         HORIZONTAL_SIZE = msg.HORIZONTAL_SIZE;
         VERTICAL_SIZE = msg.VERTICAL_SIZE;
         if (color == '' || game_state == 1 || game_state == 3 || game_state == 5) {
            if (color == '') {
               game_state = 2;
            }
            color = msg.color;
            document.querySelector('#color').innerHTML = 'Hello ' + uname + '. You are ' + color + ', now is your turn.';
            cvs.onclick = putChess;
         }
         cvs.width = HORIZONTAL_SIZE * GRID_SIZE;
         cvs.height = VERTICAL_SIZE * GRID_SIZE;
         document.getElementById('set').disabled = false;
         initCheckerBoard();
         drawCheckerBoard();
         user_name = msg.content;
         name_list = msg.user_list;
         change_type = msg.type;
         temp_color = msg.color;
         dealUser(user_name, change_type, name_list, temp_color);
         sender = 'Sys Msg: ';
         msg.content = 'Game Start!'
         break;

      case 'init_ai_vs_ai':
         HORIZONTAL_SIZE = msg.HORIZONTAL_SIZE;
         VERTICAL_SIZE = msg.VERTICAL_SIZE;

         color = msg.color;
         document.querySelector('#color').innerHTML = 'Hello ' + uname + '. You are in AI_vs_AI game, press Enter to start';
         cvs.onclick = null;

         cvs.width = HORIZONTAL_SIZE * GRID_SIZE;
         cvs.height = VERTICAL_SIZE * GRID_SIZE;
         document.getElementById('set').disabled = false;
         initCheckerBoard();
         drawCheckerBoard();
         user_name = msg.content;
         name_list = msg.user_list;
         change_type = msg.type;
         temp_color = msg.color;
         dealUser(user_name, change_type, name_list, temp_color);
         sender = 'Sys Msg: ';
         msg.content = 'AI_vs_AI Game has initialized!'
         break;

      case 'ai_vs_ai_put':
         AI_next_x = msg.x;
         AI_next_y = msg.y;
         document.getElementById('enter').disabled = false;
         document.querySelector('#color').innerHTML = AI_next_color + " is ready to placed a stone on (" + AI_next_x + ", " + AI_next_y + "), press Enter to place";
         return;

      case 'put':
         if (color != msg.color && color != 'visitor') {
            var x = msg.x;
            var y = msg.y;
            checkerBoard_type[x][y] = msg.color;
            checkerBoard_state[x][y] = false;
            drawChess(x, y);
            document.querySelector('#color').innerHTML = 'Hello ' + uname + '. You are ' + color + ", now is your turn.";
            cvs.onclick = putChess;
         }
         return;

      case 'gameover':
         if(color!=msg.color){
            var x=msg.x;
            var y=msg.y;
            checkerBoard_type[x][y]=msg.color;
            checkerBoard_state[x][y]=false;
            drawChess(x,y);
         }
         document.querySelector('#color').innerHTML = 'Hello '+uname+'. You are ' + color+ ", now "+msg.color+" win!";
         alert(msg.color == color ? 'You win!' : 'You lose!');
         sender = 'Sys Msg: ';
         msg.content = msg.color+' Win!'
         break;
   }
   var data = sender + msg.content;
   listMsg(data);
};

ws.onerror = function() {
   var data = "Sys Msg: Error! Please refresh the page.";
   listMsg(data);
};

//When close window, logout
window.onbeforeunload = function() {
   var user_info = {
      'type': 'logout',
      'content': uname,
      'color':color
   };
   sendMsg(user_info);
   ws.close();
}

/**
 * press enter to send message
 *
 * @param event
 *
 * @returns {boolean}
 */
function confirm(event) {
   var key_num = event.keyCode;
   if (13 == key_num) {
      send();
   } else {
      return false;
   }
}

/**
 * send message and clear box
 */
function send() {
   var msg_box = document.getElementById("msg_box");
   var content = msg_box.value;
   var reg = new RegExp("\r\n", "g");
   content = content.replace(reg, "");
   var msg = {
      'content': content.trim(),
      'type': 'send'
   };
   sendMsg(msg);
   msg_box.value = '';
   // todo clear /n
}

/**
 * add message to message scroll box
 */
function listMsg(data) {
   var msg_list = document.getElementById("msg_list");
   var msg = document.createElement("p");

   msg.innerHTML = data;
   msg_list.appendChild(msg);
   msg_list.scrollTop = msg_list.scrollHeight;
}

/**
 * login and out message notify
 *
 * @param user_name
 * @param type  login/logout
 * @param name_list
 */
function dealUser(user_name, type, name_list,temp_color) {
   var user_list = document.getElementById("user_list");
   var user_num = document.getElementById("user_num");
   while (user_list.hasChildNodes()) {
      user_list.removeChild(user_list.firstChild);
   }

   for (var index in name_list) {
      var user = document.createElement("p");
      user.innerHTML = name_list[index];
      user_list.appendChild(user);
   }
   user_num.innerHTML = name_list.length;
   user_list.scrollTop = user_list.scrollHeight;

   var change = type == 'logout' ? 'offline':'online'  ;

   var data = 'Sys Msg: (' +temp_color+')' +user_name + ' is ' + change;
   listMsg(data);
   if(temp_color != 'visitor' && type=='logout'){
      alert(temp_color+ ' leaves the game!');
   }
}

/**
 * transfer data to json
 * @param msg
 */
function sendMsg(msg) {
   var data = JSON.stringify(msg);
   ws.send(data);
}

/**
 * get ramdon id's postfix
 * @param msg
 */
function uuid(len, radix) {
   var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
   var uuid = [],
       i;
   radix = radix || chars.length;

   if (len) {
      for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
   } else {
      var r;

      uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
      uuid[14] = '4';

      for (i = 0; i < 36; i++) {
         if (!uuid[i]) {
            r = 0 | Math.random() * 16;
            uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
         }
      }
   }
   return uuid.join('');
}

/**
 * initial checkboard
 */
function initCheckerBoard(){

   if(color =='visitor'){
      return;
   }
   for(var i=0; i< VERTICAL_SIZE; i++){

      checkerBoard_state[i]= new Array();
      checkerBoard_type[i]= new Array();

   }
      for(var i=0; i< VERTICAL_SIZE; i++){
         for(var j=0; j< HORIZONTAL_SIZE; j++){
            checkerBoard_state[i][j]=true;
            checkerBoard_type[i][j]='';
         }
      }
   document.getElementById('set').disabled = true;
   console.log('2 players,init');
}


/**
 * event of putting chess
 * @param e
 */
function putChess(e){
   console.log('draw a chess');
   var x = parseInt((e.pageX - cvs.offsetLeft) / GRID_SIZE);
   var y = parseInt((e.pageY - cvs.offsetTop) / GRID_SIZE);
   console.log(x, y);
   var random = randomPut(x,y);
   x=random[0];
   y=random[1];

   // only when game start can putchess, otherwise return
   if(checkerBoard_state[x][y]) {
      document.querySelector('#color').innerHTML = 'Hello ' + uname + '. You are ' + color + ", now is opponent turn.";
      cvs.onclick = null;
      checkerBoard_type[x][y] = color;
      checkerBoard_state[x][y] = false;
      var msg = {
         'x': x,
         'y': y,
         'color': color,
         'type': 'put'
      };
      sendMsg(msg);
      drawChess(x, y);
      console.log(x, y);
   } else {
      console.log('not vaild place');
   }

 //  document.getElementById('tips').innerText = 'Now ' +( turn ==false? 'Black' : 'White') +' Turn!'
}

/**
 * draw chess
 */
function drawChess(x, y){
   ctx.beginPath();
   ctx.fillStyle = (checkerBoard_type[x][y] =='white' ? '#eee':'#000');
   ctx.arc((x + 0.5) * GRID_SIZE, (y + 0.5) * GRID_SIZE, (GRID_SIZE / 2) * 0.9, 0, 2 * Math.PI);
   ctx.fill();
   ctx.closePath();
}

/**
 * draw checkerboard
 */
function drawCheckerBoard(){
   ctx.beginPath();
   ctx.strokeStyle = '#000';
   ctx.fillStyle = '#FF9F33';
   ctx.fillRect(0, 0, cvs.width, cvs.height)
   for(var i = 0; i < HORIZONTAL_SIZE; i++){
      for(var j = 0; j < VERTICAL_SIZE; j++){
         ctx.strokeRect(i *GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE)
      }
   }
   ctx.closePath();
}

document.getElementById('set').onclick = function(){
    var ver=document.getElementById("ver").value;
   var hor = document.getElementById("hor").value;
   var msg = {
      'ver': ver,
      'hor': hor,
      'type': 'set'
   };
   alert('Update checkerboard size success.')
   sendMsg(msg);
}

document.getElementById('vs_random').onclick = function () {
   var msg = {
      'type': 'vs_random',
      'content': uname
   };
   game_state = 3;
   sendMsg(msg);
}

document.getElementById('vs_tree_ai').onclick = function () {
   var msg = {
      'type': 'vs_tree_ai',
      'content': uname
   };
   game_state = 1;
   sendMsg(msg);
}

document.getElementById('vs_nn_ai').onclick = function () {
   var ver = document.getElementById("ver").value;
   var hor = document.getElementById("hor").value;
   if (ver == hor && (ver == 10 || ver == 12 || ver == 14 || ver == 16 || ver == 18)) {

      var msg = {
         'type': 'vs_nn_ai',
         'content': uname
      };
      game_state = 5;
      sendMsg(msg);

   } else {
      alert('Size should be one of 10x10, 12x12, 14x14, 16x16, 18x18')
   }
}

document.getElementById('nn_ai_vs_nn_ai').onclick = function () {
   var ver = document.getElementById("ver").value;
   var hor = document.getElementById("hor").value;
   if (ver == hor && (ver == 10 || ver == 12 || ver == 14 || ver == 16 || ver == 18)) {

      var msg = {
         'type': 'nn_ai_vs_nn_ai',
         'content': uname
      };
      game_state = 6;
      sendMsg(msg);

   } else {
      alert('Size should be one of 10x10, 12x12, 14x14, 16x16, 18x18')
   }
}

document.getElementById('tree_ai_vs_tree_ai').onclick = function () {
   var ver = document.getElementById("ver").value;
   var hor = document.getElementById("hor").value;
   if (ver == hor && (ver == 10 || ver == 12 || ver == 14 || ver == 16 || ver == 18)) {

      var msg = {
         'type': 'tree_ai_vs_tree_ai',
         'content': uname
      };
      game_state = 7;
      sendMsg(msg);

   } else {
      alert('Size should be one of 10x10, 12x12, 14x14, 16x16, 18x18')
   }
}


document.getElementById('nn_ai_vs_tree_ai').onclick = function () {
   var ver = document.getElementById("ver").value;
   var hor = document.getElementById("hor").value;
   if (ver == hor && (ver == 10 || ver == 12 || ver == 14 || ver == 16 || ver == 18)) {

      var msg = {
         'type': 'nn_ai_vs_tree_ai',
         'content': uname
      };
      game_state = 4;
      sendMsg(msg);

   } else {
      alert('Size should be one of 10x10, 12x12, 14x14, 16x16, 18x18')
   }
}


document.getElementById('enter').onclick = function () {
   if (game_state != 3) {
      game_state = 3;
   } else {
      checkerBoard_type[AI_next_x][AI_next_y] = AI_next_color;
      checkerBoard_state[AI_next_x][AI_next_y] = false;
      drawChess(AI_next_x, AI_next_y);
      document.querySelector('#color').innerHTML = AI_next_color + " has placed a stone on (" + AI_next_x + ", " + AI_next_y + ")";
      AI_next_color = (AI_next_color == "black") ? "white" : "black"
   }
   document.getElementById('enter').disabled = true;
   var msg = {
      'type': 'ai_vs_ai_put',
      'content': uname,
      'color': AI_next_color
   };

   sendMsg(msg);
   document.querySelector('#color').innerHTML = AI_next_color + " is thinking.....";
   wait(2000);
}

/**
 * find available adjacent block
 */
function findAdjcblock(x, y) {
   var i = 0;
   if (x - 1 > 0 && checkerBoard_state[x - 1][y] == true) {
      adjacentBlock[i++] = [x - 1, y];
   }
   if (x + 1 < HORIZONTAL_SIZE && checkerBoard_state[x + 1][y] == true) {
      adjacentBlock[i++]=[x+1,y];
   }
   if(y-1>0 && checkerBoard_state[x][y-1]==true){
      adjacentBlock[i++]=[x,y-1];
   }
   if(y+1<VERTICAL_SIZE && checkerBoard_state[x][y+1]==true){
      adjacentBlock[i]=[x,y+1];
   }
}

/**
 * get random integer from[min,max]
 */
function randomNum(minNum,maxNum){
   switch(arguments.length){
      case 1:
         return parseInt(Math.random()*minNum+1,10);
         break;
      case 2:
         return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
         break;
      default:
         return 0;
         break;
   }
}

/**
 * random put disabled
 */
function randomPut(x,y) {
   // findAdjcblock(x,y);
   // var size= adjacentBlock.length;
   // console.log(size);
   // if(size!=0 && randomNum(0,3)>2){
   //    index = randomNum(0,size-1);
   //    x=adjacentBlock[index][0];
   //    y=adjacentBlock[index][1];
   // }
   // adjacentBlock = [];
   return [x, y]
}


