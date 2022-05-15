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
md-buttonのクラスからインスタンス化されたものを定義している。このインスタンス名前はdraw
,id=でインスタンスの名前をつけることが多い -->
        <md-button
          id="draw"
          class="md-icon-button md-primary"
          v-on:click="onDraw"
        >
<!-- clickは属性（クラスの中で定義されている）
id, classも属性
ここをクリックすると、Ondrowが呼び出される。関数
定義されたがonDrawで、それがclickにbindされている -->
          <md-icon class="md-size-2x">border_color</md-icon>
        </md-button>
        <md-button
          id="erase"
          class="md-icon-button md-primary"
          v-on:click="onErase"
        >
          <md-icon class="md-size-2x">auto_fix_normal</md-icon>
        </md-button>
        <md-button
          id="undo"
          class="md-icon-button md-primary"
          v-on:click="onUndo"
        >
          <md-icon class="md-size-2x">undo</md-icon>
        </md-button>
        <md-button
          id="redo"
          class="md-icon-button md-primary"
          v-on:click="onRedo"
        >
          <md-icon class="md-size-2x">redo</md-icon>
        </md-button>
        <md-button
          id="clear"
          class="md-icon-button md-primary"
          v-on:click="onClearCanvas"
        >
          <md-icon class="md-size-2x">clear</md-icon>
        </md-button>
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

<!-- 下は無印のファイルを示している
modeでbindさせている
無印の方にbindされている
無印からコピペしてきたようなもの
greyscaleを追記
代わりにbrushsize消去する------------------------------------------------------>
      <PaintCanvas
        ref="paintCanvas"
        :mode="mode"
        :brushColor="brushColor"
        :greyscale="greyscale"
        :eraserSize="eraserSize"
      />
      <!-- <PaintCanvas
        ref="paintCanvas"
        :mode="mode"
        :brushColor="brushColor"
        :brushSize="brushSize"
        :greyscale="greyscale"
        :eraserSize="eraserSize"
      /> -->
    </div>
    <div>
      <div>
        <label>Brush color:</label>
        <input
          type="range"
          v-model.number="brushColor"
          :min="0"
          :max="255"
        >
        <!-- <label>Brush size:</label>
        <input
          type="range"
          v-model.number="brushSize"
          :min="0"
          :max="36"
        >
        ここの部分をグレースケールに変えて、maxは255.
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
  data: () => ({
    mode: "",  //このmodeはHTMLにbindされているので、JSの中のmodeを変えると、HTMLにも反映される
    // brushColor: "",
    brushColor: 0,
    // brushSize: 3,
    greyscale: 0,  //追記
    eraserSize: 20,
    defaultMode: "brush",
    defaultBrushColor: "#000",
    currentAction: "draw"
  }),
  mounted: function() {
    // 初期化
    this.init();
    let imgSrc =
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPAgMAAABGuH3ZAAAAAXNSR0IArs4c6QAAAAlQTFRFAAANAAAA/PxQjQj98QAAAAF0Uk5TAEDm2GYAAAABYktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH2gwXFQ4DaigKYQAAADhJREFUCNdjYBANYGBgzFrKwMC2apUDg1TUtAkQImvVqiXoROaqlUsYpLKWAZVMjZoA0QHWCzIFAJGSGI4XxkZDAAAAAElFTkSuQmCC";
    this.setCanvasBackwrite(imgSrc);
  },
  methods: {
    init: function() {
      this.mode = this.defaultMode;
      this.brushColor = this.defaultBrushColor;
      this.onAction("draw");
      this.currentAction = "draw";
    },
    onDraw: function() {
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
