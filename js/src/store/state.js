export default {
  page_name: '',
  error_msg: undefined,
  algorithms: ['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN', 'Running', 'Reserved'],

  // show nav bar or not
  navigation_bar_shown_flag: false,

  // show add model modal
  add_model_modal_shown_flag: false,

  model_list: [],
  dataset_list: [],

  selected_model_id: undefined,

  /**
  * dashboard
  */
  // model ratio bar
  model_counts_per_algorith: {
    'C-GCNN': 0,
    'Kernel-GCNN': 0,
    'DBSCAN-GCNN': 0,
    'Running': 0,
    'Reserved': 0
  },

  // running models
  running_models: [],

  // sort key
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

  /**
  * prediction
  */
  pred_x: undefined,
  pred_y: undefined
}
