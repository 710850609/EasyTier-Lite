<template>
  <Layout />
</template>

<script setup>
import Layout from './components/Layout.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--color-body);
  color: var(--color-text);
  transition: background-color 0.3s, color 0.3s;
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-surface-container-low);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--color-outline);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-on-surface-variant);
}

/* MD3 主题变量适配 */
:root {
  --app-primary: var(--color-primary);
}

/* 隐藏 Snackbar 图标 */
.var-snackbar__icon {
  display: none !important;
}

/* ========== Varlet 组件全局样式适配 ========== */

/* var-select 下拉框样式适配 */
.var-select__control {
  background: var(--color-surface-container) !important;
  color: var(--color-on-surface) !important;
}

.var-select__label {
  color: var(--color-on-surface-variant) !important;
}

.var-select__placeholder {
  color: var(--color-on-surface-variant) !important;
}

.var-select__menu {
  background: var(--color-surface-container) !important;
  /* 覆盖 Varlet option 的文字颜色变量 */
  --option-text-color: var(--color-on-surface);
  --option-selected-background: var(--color-primary-container);
}

.var-option {
  color: var(--color-on-surface) !important;
}

.var-option--selected {
  background: var(--color-primary-container) !important;
  color: var(--color-on-primary-container) !important;
}

.var-option:hover {
  background: var(--color-surface-container-high) !important;
}

/* var-tabs 样式适配 */
.var-tabs {
  background: transparent !important;
}

.var-tab {
  color: var(--color-on-surface-variant) !important;
}

.var-tab--active {
  color: var(--color-primary) !important;
}

.var-tabs-indicator {
  background: var(--color-primary) !important;
}

/* var-checkbox 文字颜色适配 */
.var-checkbox__text {
  color: var(--color-on-surface) !important;
}

.var-checkbox--disabled .var-checkbox__text {
  color: var(--color-on-surface-variant) !important;
}

/* var-paper 背景适配 */
.var-paper {
  background: var(--color-surface-container) !important;
}

/* var-popup 背景适配 */
.var-popup__content {
  background: var(--color-surface-container) !important;
}

/* var-cell 样式适配 */
.var-cell {
  color: var(--color-on-surface) !important;
}

.var-cell__description {
  color: var(--color-on-surface-variant) !important;
}
</style>