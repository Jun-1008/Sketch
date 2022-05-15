<template>
  <div>
    <div
      ref="container"
      class="container"
    />
    <div
      ref="layers_previewer"
      class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
    >
    </div>
  </div>
</template>

<script>
// 上のrefはidとして書いても良い。loaderの中ではidとして書かれた例があり
import Konva from "konva";
import axios from "axios";
export default {//JSでは{}はオブジェクト生成
  name: "paint-canvas",
// 【第5ブロック】---------------------------------------------------------------------------
  props: {// ここではスケッチの領域のような、変わらないものを定義する
    mode: {
      type: String,
      default: ""
    },
    brushColor: {
      type: Number,
      // type: String,//デフォ
      default: 0
      // default: ""//デフォルト、太さの調整が可能
    },
    // brushSize: {
    grayscale: {
      type: Number,//下のdata: と異なりここでの変更は反映されなのもそれが原因？
      default: 0 //3
    },
    eraserSize: {
      type: Number,
      default: 20
    },
    backgroundImage: {
      type: String,
      default: ""
    }
  },
  data: () => ({// dataの方で変数の定義。propsと違いアプリが動いている時に変わりそうな値
    stage: null, //クラスの要素
    context: null,
    canvasGroup: [],
    drawingLayer: null,
    lastPointerPosition: {},
    isPaint: false,
    undoStack: [],
    redoStack: [],
    paint_history: [],  //記述はあるがコメントアウト
    pen_history: [],  //184行目にthis.pen_historyの形で記述あり
    layerCount: 1,
    layerActive: 0,
    width: 720,  //この2つでスケッチさせる面の大きさを指定している
    height: 720
  }),
  mounted: function() {  //関数宣言。ここは関数名なし。()内は引数。以下は{}の中が処理内容
  //mountedは起動させた時に行われるプログラム
  //mountedも一つの関数
    var container = this.$refs.container;  //変数宣言。var 変数名＝値
    //一番上でref= 名前をつけたモノは、全て$sで代入される
    //なのでここではthis.container.container と同じ
    //定義というよりHTMLのエレメントを呼び出している
    //エレメント＝属性と似たような概念    
    this.stage = new Konva.Stage({  //上のdataブロックの中でstage:nullが明記
    //インスタンス化。stageもKonvaの中の１つのクラス
    //this要素を指定している
      container,
      width: this.width,
      height: this.width
    });
    this.drawingLayer = new Konva.Layer();  //drawingLayerの要素を定義している
    this.stage.add(this.drawingLayer);

    this.canvasGroup.push(this.drawingScope());
    this.previewLayer();
  },
  methods: {  //コロンの意味は、{}の中の説明
  // 複数の関数を定義している
    drawingScope: function() {  //drawingScopeの役割は？
      let canvas = document.createElement("canvas");  //letも変数宣言。しかし再宣言するとエラーになり、if文の中などでも使うことができない
      canvas.ref = "canvas_" + this.layerCount;
      canvas.width = this.width;
      canvas.height = this.height;
      let drawingScope = new Konva.Image({
        image: canvas
      });
      this.drawingLayer.add(drawingScope);
      this.stage.draw();
// 【第6ブロック】--------------------------------------------------------------------------------------------------------------------------------------------
      this.context = canvas.getContext("2d");
      this.context.strokeStyle = this.brushColor;  //strokestyleで線の色を変える事が出来る
      this.context.lineJoin = "round";
      this.context.strokeStyle = this.grayscale;  //
      // this.context.lineWidth = this.brushSize;  //左辺のlineWidthが線の太さ。brushsizeは最初の方のpropsの中で登場. 
      // this.context.lineWidth = this.grayscale;  //デフォルト


      // add event
      drawingScope.on("mousedown", this.mousedown);
      this.stage.addEventListener("mouseup", this.mouseup);
      this.stage.addEventListener("mousemove", this.mousemove);
      drawingScope.on("touchstart", this.mousedown);
      this.stage.addEventListener("touchend", this.mouseup);
      this.stage.addEventListener("touchmove", this.mousemove);

      return canvas;
    },
    mousedown: function() {  //マウスを押した時の挙動
      this.isPaint = true;
      this.lastPointerPosition = this.stage.getPointerPosition();
      this.undoStack.push({
        layer: this.layerActive,
        content: this.context.getImageData(0, 0, this.width, this.height)
      });
    },
    mouseup: function() {  //マウスを離したらthis.isPaintをfalseにしている
      this.isPaint = false;

    //   axios
    //     .post("https://www.ultratks.live/api/sketch/stroke/save_stroke", {
    //       request_type: "save_stroke",
    //       pen_history: this.pen_history
    //     })
    //     .then(function(response) {
    //       if (response.data.response_type === "save_confirmed") {
    //         console.log("save confirmed");
    //       } else {
    //         throw Error("Failed. Please contact the server admin.");
    //       }
    //     })
    //     .catch(function(error) {
    //       console.log(error);
    //       self.operation = "Confirm";
    //     });
    //   this.pen_history = [];
    },
    mousemove: function() {  //押している間の動き
      if (!this.isPaint) {
        return;
      }
      if (this.isTargetMode("brush")) {
        this.context.globalCompositeOperation = "source-over";
      }
      if (this.isTargetMode("eraser")) {
        this.context.globalCompositeOperation = "destination-out";
      }

      // get image data before paint
      // let image_data_before = this.context.getImageData(
      //   0,
      //   0,
      //   this.width,
      //   this.height
      // ).data;

      this.context.beginPath();

      let localPos = {
        x: 0,
        y: 0
      };

      localPos.x = this.lastPointerPosition.x;
      localPos.y = this.lastPointerPosition.y;
      let last_pos = { x: localPos.x, y: localPos.y };

      this.context.moveTo(localPos.x, localPos.y);

      let pos = this.stage.getPointerPosition();
      localPos.x = pos.x;
      localPos.y = pos.y;

      this.context.lineTo(localPos.x, localPos.y);
      this.context.closePath();
      this.context.stroke();
      this.drawingLayer.draw();

      this.lastPointerPosition = pos;

      // get image data before paint
      // let image_data_after = this.context.getImageData(
      //   0,
      //   0,
      //   this.width,
      //   this.height
      // ).data;

      // save history as json
      // this.paint_history.push({
      //   layer: this.layerActive,
      //   before: image_data_before,
      //   after: image_data_after
      // });
      this.pen_history.push({
        layer: this.layerActive,
        last_pen_position: last_pos,
        now_pen_position: { x: pos.x, y: pos.y }
      });
    },
    onClearCanvas: function() {  //
      this.undoStack.push({
        layer: this.layerActive,
        content: this.context.getImageData(0, 0, this.width, this.height)
      });
      this.context.globalCompositeOperation = "destination-out";
      this.context.fillRect(0, 0, this.stage.width(), this.stage.height());
      this.drawingLayer.draw();
    },
    isTargetMode: function(targetMode) {
      return this.mode === targetMode;
    },
    undo: function() {
      if (this.undoStack.length <= 0) {
        return;
      }

      this.redoStack.push({
        layer: this.layerActive,
        content: this.context.getImageData(0, 0, this.width, this.height)
      });

      this.context.putImageData(this.undoStack.pop().content, 0, 0);
      this.drawingLayer.draw();
    },  //ここまでmousemodeの説明
    redo: function() {
      if (this.redoStack.length <= 0) {
        return;
      }

      this.undoStack.push({
        layer: this.layerActive,
        content: this.context.getImageData(0, 0, this.width, this.height)
      });

      this.context.putImageData(this.redoStack.pop().content, 0, 0);
      this.drawingLayer.draw();
    },
    addLayer: function() {
      this.canvasGroup.push(this.drawingScope());
      this.layerCount++;
      this.layerActive++;
      this.previewLayer();
    },
    removeLayer: function() {
      this.drawingLayer.get(this.layerCount).destroy();
      this.drawingLayer.draw();
      this.layerCount--;
      this.layerActive--;
      this.previewLayer();
    },
    previewLayer: function() {
      let layer_previewer = this.$refs.layers_previewer;
      while (layer_previewer.firstChild) {
        layer_previewer.removeChild(layer_previewer.firstChild);
      }
      for (let idx = 0; idx < this.canvasGroup.length; idx++) {
        // var image = new Image();
        // image.id = "preview_layer_" + idx;
        // image.src = this.canvasGroup[idx].toDataURL();

        let layer_preview_button = document.createElement("button");
        layer_preview_button.id = "btn_layer_" + idx;
        layer_preview_button.innerHTML = "layer_" + idx;
        layer_previewer.onclick = this.onBtnLayerClick;

        layer_previewer.appendChild(layer_preview_button);
      }
    },
    onBtnLayerClick: function(e) {
      this.layerActive = Number(e.srcElement.id.split("_")[2]);
    },
    onSave: function() {  //消すとエラー？
      axios
        .post("https://www.ultratks.live/api/sketch/stroke/save_history", {
          request_type: "save_history"
        })
        .then(function(response) {
          if (response.data.response_type === "save_confirmed") {
            console.log("save confirmed");
          } else {
            throw Error("Failed. Please contact the server admin.");
          }
        })
        .catch(function(error) {
          console.log(error);
          self.operation = "Confirm";
        });
    },
    setCanvas: function(imgSrc) {
      // this.context.putImageData(imgObject, 0, 0);
      console.log(imgSrc);
      let self = this;
      let image = new Image();
      image.src = imgSrc;
      image.onload = function() {
        self.context.drawImage(image, 0, 0);
        self.drawingLayer.draw();
      };
    }
  },
  watch: {  //定義された値が変わった時の対応が書かれている。
// 【第7ブロック】--------------------------------------------------------------------------------------------------------
    mode: function() {
      if (this.mode === "brush") {
        // this.context.lineWidth = this.brushSize;
        this.context.strokeStyle = this.grayscale;
      } else {
        this.context.lineWidth = this.eraserSize;
      }
    },
// 【第8ブロック】----------------------------------------------------------------------------------------------------------------
    // brushColor: function() {  大元
    //   if (this.mode === "brush") {
    //     this.context.strokeStyle = this.brushColor;//strokestyleで線の色を変える
    //   }
    // },
    // // ---------------------------------------------------------------------
    brushColor: function() {
      if (this.mode === "brush") {
        // color の数字を１６進数の色のカラーコードに変換。
        // color = this.colorConverter(this.brushColor);//必要？
        // this.context.strokeStyle = 'red'; //strokestyleで線の色を変える.ここに追記！！！！！！！！！！！！
        // this.context.strokeStyle = this.brushColor; //ここに追記！！！！！！！！！！！！
        this.context.strokeStyle = 0x808080; //ここに追記！！！！！！！！！！！！

        // this.context.strokeStyle = color; //デフォルト
        // this.context.strokeStyle = this.brushColor;
      }
    },
    // // ---------------------------------------------------------------------
        // brushSize: function() {
    grayscale: function() {
      if (this.mode === "brush") {
        // this.context.lineWidth = this.grayscale; //左辺のlineWidthが線の太さ。strokeStyle
        this.context.strokeStyle = this.grayscale; //左辺のlineWidthが線の太さ。strokeStyle
        // this.context.lineWidth = this.brushSize; //左辺のlineWidthが線の太さ。
      }
    },

    eraserSize: function() {
      if (this.mode === "eraser") {
        this.context.lineWidth = this.eraserSize;
      }
    },
    layerActive: function() {
      for (let idx = 0; idx < this.canvasGroup.length; idx++) {
        let canvas = this.canvasGroup[idx];
        let ctx = canvas.getContext("2d");

        let imageData = ctx.getImageData(0, 0, this.width, this.height);
        let pixels = imageData.data;
        if (idx === this.layerActive) {
          // TOP LAYER COLOR: BLACK

          for (let i = 0; i < pixels.length; i += 4) {
            // Is this pixel *gray* ?
            if (pixels[i] === 127) {
              pixels[i] = 0;
              pixels[i + 1] = 0;
              pixels[i + 2] = 0;
            }
          }
        } else {
          // OTHER LAYERS COLOR: GRAY

          for (let i = 0; i < pixels.length; i += 4) {
            // Is this pixel *black* ?
            if (pixels[i] === 0) {
              pixels[i] = 127;
              pixels[i + 1] = 127;
              pixels[i + 2] = 127;
            }
          }
        }
        ctx.putImageData(imageData, 0, 0);
        this.drawingLayer.draw();
      }
      this.context = this.canvasGroup[this.layerActive].getContext("2d");
      // this.context.strokeStyle = this.brushColor;
      this.context.strokeStyle = this.brushColor;
      this.context.lineJoin = "round";
      this.context.lineWidth = 3;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  border: 3px solid #000;
  max-width: 720px;
  align-items: center;
  text-align: center;
  display: inline-block;
}
</style>
<!-- container -->
<!-- 最初の<templete>htmlの中身と、起動時に実行されるmountedの部分にあり、つまり初期設定？
    ここのブラシの設定なども変更か？
    CSSで書かれている。見た目を定義している 
    HTMLはレイアウトを定義する。何がどこにあるか
    CSSはレイアウトはの文字の大きさだったり、カラーだったりを定義。たただのマークで簡単な記述しかできない
    JSはなんでもできる。JSだけでもアプリを作ることは可能
    borderはスケッチ領域を黒で囲っている
    HTMLでclass="container"となっているものは、CSSで.クラスの中身とすると、
    そのクラス全体にコレが反映されるということになる-->