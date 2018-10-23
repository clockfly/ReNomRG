export default {
  page_name: '',
  error_msg: undefined,

  // show nav bar or not
  navigation_bar_shown_flag: false,

  // show add model modal
  add_model_modal_shown_flag: false,

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

  /**
  * Model list
  */
  model_list: [],

  // sort key
  sort_key: 0,
  // prediction model
  deployed_model_id: undefined,

  /**
  * Model Detail
  */
  selected_model_id: undefined,
  selected_model: undefined,

  /**
  * learning curve
  */
  valid_loss_list: [],
  train_loss_list: [],

  /**
  * prediction sample
  */
  selected_y_valid: [],
  selected_y_pred: [],
  deployed_model_y_valid: [],
  deployed_model_y_pred: [],

  /**
  * features
  */
  // data
  labels: [],

  /**
  * modal params setting
  */
  dataset_name_list: [],
  dataset_list: [],

  /**
  * modal dataaset setting
  */
  train_count: 0,
  valid_count: 0,
  target_train: [],
  target_valid: [],
  train_index: [],
  valid_index: [],

  /**
  * dataset page
  */
  selected_dataset_id: undefined,
  selected_dataset: undefined
}
