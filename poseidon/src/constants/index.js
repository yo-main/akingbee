
export const AUTH_COOKIE_NAME = "access_token";

export const languages = ["fr", "en"];

export const sections = {
  menu_manage: 'manage',
  menu_setup: 'setup',
  menu_profil: 'profil',
  menu_admin: 'admin',
  submenu_hive: 'submenu_hive',
  submenu_hive_list: 'submenu_hive_list',
  submenu_hive_stock: 'submenu_hive_stock',
  submenu_hive_create: 'submenu_hive_create',
  submenu_apiary: 'submenu_apiary',
  submenu_apiary_list: 'submenu_apiary_list',
  submenu_apiary_create: 'submenu_apiary_create',
  submenu_setup_swarm: 'submenu_setup_swarm',
  submenu_setup_swarm_health: 'submenu_setup_swarm_health',
  submenu_setup_hive: 'submenu_setup_hive',
  submenu_setup_hive_beekeeper: 'submenu_setup_hive_beekeeper',
  submenu_setup_hive_condition: 'submenu_setup_hive_condition',
  submenu_setup_apiary: 'submenu_setup_apiary',
  submenu_setup_apiary_honey_kind: 'submenu_setup_apiary_honey_kind',
  submenu_setup_event: 'submenu_setup_event',
  submenu_setup_event_type: 'submenu_setup_event_type',
  submenu_setup_event_status: 'submenu_setup_event_status',
};

export const setupData = {
  swarm_health_status: "swarm_health",
  hive_beekeeper: "owner",
  hive_condition: "hive_condition",
  apiary_honey_kind: "honey_kind",
  event_type: "event_type",
  event_status: "event_status",
}

export const formItemLayoutWithoutLabel = {
  wrapperCol: {
    xs: { span: 24, offset: 0 },
    sm: { span: 20, offset: 8 },
  },
};

export const formItemLayout = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 8 },
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 16 },
  },
};

export const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 16,
      offset: 8,
    },
  },
};

export const passwordValidationRules = [
  {min: 8, message: window.i18n('form.heightCharactersMinimum')},
  {pattern: ".*[0-9]+.*", message: window.i18n('form.mustIncludeOneDigit')},
  {pattern: ".*[a-zA-Z]+.*", message: window.i18n('form.mustIncludeOneLetter')},
  {required: true, message: window.i18n('form.insertPasswordMessage')}
]

