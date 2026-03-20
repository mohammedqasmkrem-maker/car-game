<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>Pro Car Game</title>

<style>
body {
  margin: 0;
  overflow: hidden;
  font-family: Arial;
  background: black;
}

/* خلفية */
#bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(#0f2027, #203a43, #2c5364);
  animation: bgMove 10s infinite alternate;
}

@keyframes bgMove {
  from { filter: brightness(0.7); }
  to { filter: brightness(1.2); }
}

/* الطريق */
#road {
  position: absolute;
  width: 320px;
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #111;
  border-left: 4px solid cyan;
  border-right: 4px solid cyan;
  box-shadow: 0 0 30px cyan;
  overflow: hidden;
}

/* خطوط الطريق */
.line {
  position: absolute;
  width: 6px;
  height: 60px;
  background: white;
  left: 50%;
  transform: translateX(-50%);
  animation: moveLine 0.4s linear infinite;
}

@keyframes moveLine {
  from { top: -60px; }
  to { top: 100%; }
}

/* السيارة */
#car {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 70px;
  filter: drop-shadow(0 0 20px cyan);
}

/* UI */
#ui {
  position: absolute;
  width: 100%;
  top: 10px;
  display: flex;
  justify-content: space-around;
}

.box {
  background: rgba(0,0,0,0.5);
  padding: 10px 20px;
  border-radius: 15px;
  color: cyan;
  font-size: 20px;
  border: 1px solid cyan;
  box-shadow: 0 0 15px cyan;
}

/* أزرار */
.controls {
  position: absolute;
  bottom: 20px;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.btn {
  width: 90px;
  height: 90px;
  margin: 20px;
  border-radius: 50%;
  background: rgba(0,255,255,0.1);
  color: white;
  font-size: 35px;
  text-align: center;
  line-height: 90px;
  border: 2px solid cyan;
  backdrop-filter: blur(10px);
  transition: 0.2s;
}

.btn:active {
  transform: scale(1.2);
  background: cyan;
  color: black;
  box-shadow: 0 0 20px cyan;
}
</style>
</head>

<body>

<div id="bg"></div>

<div id="road">
  <div class="line"></div>
</div>

<img id="car" src="https://cdn-icons-png.flaticon.com/512/743/743922.png">

<div id="ui">
  <div class="box">⭐ <span id="score">0</span></div>
  <div class="box">⚡ <span id="speed">0</span></div>
</div>

<div class="controls">
  <div class="btn" id="left">⬅</div>
  <div class="btn" id="right">➡</div>
</div>

<script>
let car = document.getElementById("car");
let score = 0;
let speed = 0;

/* تحكم */
document.getElementById("left").onclick = () => {
  car.style.left = (car.offsetLeft - 25) + "px";
};

document.getElementById("right").onclick = () => {
  car.style.left = (car.offsetLeft + 25) + "px";
};

/* تحديث */
function gameLoop() {
  score++;
  speed += 0.05;

  document.getElementById("score").innerText = score;
  document.getElementById("speed").innerText = Math.floor(speed);

  requestAnimationFrame(gameLoop);
}
gameLoop();
</script>

</body>
</html>
