/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <transition name="modal">
    <div
      class="modal-mask"
      @click="$emit('cancel')"
    >
      <div class="modal-wrapper">
        <div class="modal-container">
          <slot name="contents">
            default content
          </slot>

          <div class="modal-footer">
            <slot name="footer">
              <slot name="okbutton">
                <button
                  class="button-ok"
                  @click="$emit('ok')"
                >
                  OK
                </button>
              </slot>
              <slot name="cancelbutton">
                <button
                  class="button-cancel"
                  @click="$emit('cancel')"
                >
                  Cancel
                </button>
              </slot>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'ModalBox',
  mounted: function () {
    document.getElementsByClassName('button-ok')[0].focus()
  }
}
</script>

<style lang="scss" scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 500px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 0px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

.modal-footer {
  margin: 20px 10px 0px 10px;
  text-align: right;
}
</style>
