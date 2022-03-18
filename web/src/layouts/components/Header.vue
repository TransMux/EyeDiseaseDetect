<template>
  <div :class="layoutCls">
    <t-head-menu :class="menuCls" :theme="theme" expand-type="popup" :value="active">
      <div class="dev-pointer">Development mode</div>
      <MenuContent v-show="layout !== 'side'" class="header-menu" :nav-data="menu" />
      <template #operations>
        <div class="operations-container">
          <!-- 搜索框 -->
          <!-- <search v-if="layout !== 'side'" :layout="layout" /> -->

          <!-- 全局通知 -->
          <!-- <notice /> -->

          <t-tooltip placement="bottom" content="代码仓库">
            <t-button theme="default" shape="square" variant="text" @click="navToGitHub">
              <t-icon name="logo-github" />
            </t-button>
          </t-tooltip>
          <t-tooltip placement="bottom" content="帮助文档">
            <t-button theme="default" shape="square" variant="text" @click="navToHelper">
              <t-icon name="help-circle" />
            </t-button>
          </t-tooltip>
          <!-- <t-tooltip placement="bottom" content="系统设置">
            <t-button theme="default" shape="square" variant="text">
              <t-icon name="setting" @click="toggleSettingPanel" />
            </t-button>
          </t-tooltip> -->
        </div>
      </template>
    </t-head-menu>
  </div>
</template>

<script setup lang="ts">
import { PropType, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useSettingStore } from '@/store';
import { prefix } from '@/config/global';
import { MenuRoute } from '@/interface';

import MenuContent from './MenuContent';

const props = defineProps({
  theme: {
    type: String,
    default: '',
  },
  layout: {
    type: String,
    default: 'top',
  },
  menu: {
    type: Array as PropType<MenuRoute[]>,
    default: () => [],
  },
  isFixed: {
    type: Boolean,
    default: false,
  },
  isCompact: {
    type: Boolean,
    default: false,
  },
  maxLevel: {
    type: Number,
    default: 3,
  },
});

// const router = useRouter();
// const settingStore = useSettingStore();

// const toggleSettingPanel = () => {
//   settingStore.updateConfig({
//     showSettingPanel: true,
//   });
// };

const active = computed(() => {
  const route = useRoute();
  if (!route.path) {
    return '';
  }
  return route.path
    .split('/')
    .filter((item, index) => index <= props.maxLevel && index > 0)
    .map((item) => `/${item}`)
    .join('');
});

const layoutCls = computed(() => [`${prefix}-header-layout`]);

const menuCls = computed(() => {
  const { isFixed, layout, isCompact } = props;
  return [
    {
      [`${prefix}-header-menu`]: !isFixed,
      [`${prefix}-header-menu-fixed`]: isFixed,
      [`${prefix}-header-menu-fixed-side`]: layout === 'side' && isFixed,
      [`${prefix}-header-menu-fixed-side-compact`]: layout === 'side' && isFixed && isCompact,
    },
  ];
});

const navToGitHub = () => {
  // window.open('https://github.com/tencent/tdesign-vue-next-starter');
};

const navToHelper = () => {
  // window.open('http://tdesign.tencent.com/starter/docs/get-started');
};
</script>
<style lang="less">
@import '@/style/variables.less';

.dev-pointer {
  position: absolute;
  font: bold;
  color: var(--td-error-color-6);
}

.@{prefix}-header {
  &-layout {
    height: 64px;
  }

  &-menu-fixed {
    position: fixed;
    top: 0;
    z-index: 10;

    &-side {
      left: 232px;
      right: 0;
      z-index: 10;
      width: auto;
      transition: all 0.3s;

      &-compact {
        left: 64px;
      }
    }
  }

  &-logo-container {
    cursor: pointer;
    display: inline-flex;
    height: 64px;
  }
}
.header-menu {
  flex: 1 1 1;
  display: inline-flex;
  margin: auto;
}

.operations-container {
  display: flex;
  align-items: center;
  margin-right: 12px;

  .t-popup__reference {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .t-button {
    margin: 0 8px;
    &.header-user-btn {
      margin: 0;
    }
  }

  .t-icon {
    font-size: 20px;
    &.general {
      margin-right: 16px;
    }
  }
}

.header-operate-left {
  display: flex;
  margin-left: 20px;
  align-items: normal;
  line-height: 0;

  .collapsed-icon {
    font-size: 20px;
  }
}

.header-logo-container {
  width: 184px;
  height: 26px;
  display: flex;
  margin-left: 24px;
  color: @text-color-primary;

  .t-logo {
    width: 100%;
    height: 100%;
    &:hover {
      cursor: pointer;
    }
  }

  &:hover {
    cursor: pointer;
  }
}

.header-user-account {
  display: inline-flex;
  align-items: center;
  color: @text-color-primary;
  .t-icon {
    margin-left: 4px;
    font-size: 16px;
  }
}

.t-head-menu__inner {
  border-bottom: 1px solid @border-level-1-color;
}

.t-menu--light {
  .header-user-account {
    color: @text-color-primary;
  }
}
.t-menu--dark {
  .t-head-menu__inner {
    border-bottom: 1px solid var(--td-gray-color-10);
  }
  .header-user-account {
    color: rgba(255, 255, 255, 0.55);
  }
  .t-button {
    --ripple-color: var(--td-gray-color-10) !important;
    &:hover {
      background: var(--td-gray-color-12) !important;
    }
  }
}

.operations-dropdown-container-item {
  width: 100%;
  display: flex;
  align-items: center;

  .t-icon {
    margin-right: 8px;
  }

  .t-dropdown__item {
    .t-dropdown__item__content {
      display: flex;
      justify-content: center;
    }
    .t-dropdown__item__content__text {
      display: flex;
      align-items: center;
      font-size: 14px;
    }
  }

  .t-dropdown__item {
    width: 100%;
    margin-bottom: 0px;
  }
  &:last-child {
    .t-dropdown__item {
      margin-bottom: 8px;
    }
  }
}
</style>
