export default {
  page_name: '',
  error_msg: undefined,
  algorithms: {
    0: 'C-GCNN',
    1: 'Kernel-GCNN',
    2: 'DBSCAN-GCNN',
    3: 'Random-Forest',
    0xffffffff: 'user-defined'
  },

  // show nav bar or not
  navigation_bar_shown_flag: false,

  // show add model modal
  add_model_modal_shown_flag: false,

  labels: [],
  model_list: [],
  dataset_list: [],
  running_models: [],

  selected_model_id: undefined,

  /**
  * dashboard
  */
  // model ratio bar
  model_counts_per_algorith: {},

  /**
  * Model List
  */
  sort_key: 0,

  /**
  * modal dataset setting
  */
  train_count: 0,
  valid_count: 0,
  target_train: [],
  target_valid: [],
  train_index: [],
  valid_index: [],
  true_histogram: [],
  scalings: {
    1: 'None scaling',
    2: 'Standardization',
    3: 'Normalization'
  },
  filename_y: undefined,
  filename_X: undefined,

  /**
  * prediction
  */
  pred_x: undefined,
  pred_y: undefined,
  pred_csv: undefined
}
