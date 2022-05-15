<template>
  <div>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/icon?family=Material+Icons"
    >
    <div
      class="md-layout md-gutter"
      style="margin-top: 30px;"
    >
      <div class="md-layout-item">
<!-- 
md-button : アイコンのようなもの、機能としてはクリックしたら定義されている関数が呼び出される
一番最初だけmd-iconが無い？
ドロー、消しゴム、全てにmd-buttonはあり
md-buttonのクラスからインスタンス化されたものを定義している。このインスタンス名前はdraw。mtgメモの白板の例
,id=でインスタンスの名前をつけることが多い
onDraw () として関数が下のmethodでJSで書かれ定義されている -->
        <md-button
          id="draw"
          class="md-icon-button md-primary"
          v-on:click="onDraw"
        >
          <md-icon class="md-size-2x">border_color</md-icon>
        </md-button>
<!-- clickは属性（クラスの中で定義されている）
id, classも属性
ここをクリックすると、Ondrowが呼び出される。関数
定義されたがonDrawで、それがclickにbindされている -->

<!-- 消しゴム -->
        <md-button
          id="erase"
          class="md-icon-button md-primary"
          v-on:click="onErase"
        >
          <md-icon class="md-size-2x">auto_fix_normal</md-icon>
        </md-button>

<!-- 左半回転矢印、１つ戻る -->
        <md-button
          id="undo"
          class="md-icon-button md-primary"
          v-on:click="onUndo"
        >
          <md-icon class="md-size-2x">undo</md-icon>
        </md-button>

<!-- 右半回転矢印、１つ進む -->
        <md-button
          id="redo"
          class="md-icon-button md-primary"
          v-on:click="onRedo"
        >
          <md-icon class="md-size-2x">redo</md-icon>
        </md-button>

<!-- Xマーク.消す -->
        <md-button
          id="clear"
          class="md-icon-button md-primary"
          v-on:click="onClearCanvas"
        >
          <md-icon class="md-size-2x">clear</md-icon>
        </md-button>

<!-- 面が重なっているマーク、クリックすると線が薄くなって追記できるようになる -->
        <md-button
          id="draw"
          class="md-icon-button md-primary"
          v-on:click="onAddLayer"
        >
          <md-icon class="md-size-2x">layers</md-icon>
        </md-button>
        <!-- TODO: remove layer -->
        <!-- <md-button
          id="draw"
          class="md-icon-button md-primary"
          v-on:click="onRemoveLayer"
        >
          <md-icon class="md-size-2x">layers_clear</md-icon>
        </md-button> -->

<!-- ☑マーク -->
        <md-button
          class="md-icon-button md-primary"
          id="save"
          v-on:click="onSave"
        >
          <md-icon class="md-size-2x">done</md-icon>
        </md-button>

      </div>
    </div>
    <div class="container">

      <!-- 以下は下側の調整バーに関する記述
下は無印のファイルを示している
modeでbindさせている
無印の方にbindされている
無印からコピペしてきたようなもの
grayscaleを追記
代わりにbrushsize消去する------------------------------------------------------>
<!-- 【第1ブロック】-------------------------------------------------------- -->
      <!-- <PaintCanvas
        ref="paintCanvas"
        :mode="mode"
        :brushColor="brushColor"
        :brushSize="brushSize"
        :eraserSize="eraserSize"
      /> -->
<!-- ----------------------------------------------------------------------------- -->
<!-- 上記4つの要素は無印のpropsで定義。ここは上ではなく下側の調整部分！！
上記はデフォでbrushColorは入っているが、以下のdivに記載がないから反映されていないのか？
refはname? 追加でbackgroundImageがある
一旦brushsizeは消去する -->
      <PaintCanvas
        ref="paintCanvas"
        :mode="mode"
        :brushColor="brushColor"
        :grayscale="grayscale"
        :eraserSize="eraserSize"
      />
    </div>
    <!-- 【第2ブロック】-------------------------------------------------- -->
    <div>
      <div>
        <!-- <label>Brush size:</label>
        <input
          type="range"
          v-model.number="brushSize"
          :min="0"
          :max="36"
        > -->
        <label>gray scale:</label>
        <input
          type="range"
          v-model.number="grayscale"
          :min="0"
          :max="255"
        >
        <!-- ここの部分をグレースケールに変えて、maxは255.
        bind先は -->
        <label>Eraser size:</label>
        <input
          type="range"
          v-model.number="eraserSize"
          :min="0"
          :max="50"
        >
      </div>
    </div>
  </div>
</template>

<script>
import PaintCanvas from "./PaintCanvas.vue";
export default {
  name: "paint-canvas-loader",
  components: { PaintCanvas },
  props: {},
  // 【第３ブロック】--------------------------------------------------------
  data: () => ({ //propsと違いアプリが動いている時に変わりそうな値
  // ここは初期値？
    mode: "",//このmodeはHTMLにbindされているので、JSの中のmodeを変えると、HTMLにも反映される
    // brushColor: "",  //デフォルト
    brushColor: 0,
    // brushSize: 3,  //デフォルト
    grayscale: 0,//上のbrushsize:3を消してこっちを表示させる
    eraserSize: 20,
    defaultMode: "brush",
    defaultBrushColor: "#000",  //このfunctionも変更の必要ありか
    currentAction: "draw"
  }),
  mounted: function() {
    // 初期化
    this.init();
    let imgSrc =
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPAgMAAABGuH3ZAAAAAXNSR0IArs4c6QAAAAlQTFRFAAANAAAA/PxQjQj98QAAAAF0Uk5TAEDm2GYAAAABYktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH2gwXFQ4DaigKYQAAADhJREFUCNdjYBANYGBgzFrKwMC2apUDg1TUtAkQImvVqiXoROaqlUsYpLKWAZVMjZoA0QHWCzIFAJGSGI4XxkZDAAAAAElFTkSuQmCC";
    this.setCanvasBackwrite(imgSrc);
  },
  // 【4ブロック】---------------------------------------------------------------------------------------
  methods: {
    init: function() {
      this.mode = this.defaultMode;
      this.brushColor = this.defaultBrushColor;
      this.onAction("draw");
      this.currentAction = "draw";
    },
    onDraw: function() {  //brushは描くペンマーク。size調整は別。html部分に機能を付与
      this.mode = "brush";
      this.onAction("draw");
    },
    onErase: function() {
      this.mode = "eraser";
      this.onAction("erase");
    },
    onClearCanvas: function() {
      this.$refs.paintCanvas.onClearCanvas();
      this.init();
    },
    onUndo: function() {
      this.$refs.paintCanvas.undo();
    },
    onRedo: function() {
      this.$refs.paintCanvas.redo();
    },
    onAction: function(targetAction) {
      if (this.currentAction !== targetAction) {
        let activatedButton = document.getElementById(this.currentAction);
        activatedButton.classList.remove("md-accent");
        activatedButton.classList.add("md-primary");
        let targetButton = document.getElementById(targetAction);
        targetButton.classList.remove("md-primary");
        targetButton.classList.add("md-accent");
        this.currentAction = targetAction;
      } else {
        let targetButton = document.getElementById(targetAction);
        targetButton.classList.remove("md-primary");
        targetButton.classList.add("md-accent");
      }
    },
    onAddLayer: function() {
      this.$refs.paintCanvas.addLayer();
    },
    onRemoveLayer: function() {
      this.$refs.paintCanvas.removeLayer();
    },
    onSave: function() {
      this.$refs.paintCanvas.onSave();
    },
    setCanvasBackwrite: function(imgSrc) {
      this.$refs.paintCanvas.setCanvas(imgSrc);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.md-field {
  max-width: 50px;
}
.md-icon-button {
  width: 72px;
  height: 72px;
}
.container {
  margin: 10px 120px;
}
</style>
