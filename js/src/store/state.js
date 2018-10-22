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
  // model_counts_per_algorith: {
  //   'C-GCNN': 0,
  //   'Kernel-GCNN': 0,
  //   'DBSCAN-GCNN': 0,
  //   'Running': 0,
  //   'Reserved': 0
  // },

  // running models
  // running_models: [],

  /**
  * Model list
  */
  // model_list: [],

  // sort key
  sort_key: 0,
  // prediction model
  deployed_model_id: undefined,

  /**
  * Model Detail
  */
  // selected_model_id: undefined,
  // selected_model: undefined,

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
  // labels: []

  /**
  * dummy data
  */
  model_list: [
    {
      'model_id': 10,
      'algorithm': 'Kernel-GCNN',
      'validation_loss': 0.9999,
      'rmse': 0.9999,
      'max_absolute_error': 0.9999
    },
    {
      'model_id': 11,
      'algorithm': 'DBSCAN-GCNN',
      'validation_loss': 0.9999,
      'rmse': 0.9999,
      'max_absolute_error': 0.9999
    },
    {
      'model_id': 12,
      'algorithm': 'C-GCNN',
      'validation_loss': 0.9999,
      'rmse': 0.9999,
      'max_absolute_error': 0.9999
    }
  ],
  model_counts_per_algorith: {
    'C-GCNN': 5,
    'Kernel-GCNN': 2,
    'DBSCAN-GCNN': 3,
    'Running': 1,
    'Reserved': 1
  },
  running_models: [
    {
      'model_id': 9999,
      'algorithm': 'Kernel-GCNN',
      'epoch': 9999,
      'total_batch': 9999,
      'last_epoch': 9999,
      'last_batch': 9999,
      'train_loss': 0.9999
    },
    {
      'model_id': 9998,
      'algorithm': 'DBSCAN-GCNN',
      'epoch': 9999,
      'total_batch': 9999,
      'last_epoch': 9999,
      'last_batch': 9999,
      'train_loss': 0.9999
    }
  ],
  selected_model_id: 10,
  selected_model: {
    'dataset_name': 'test_test_test',
    'epoch': 9999,
    'batch_size': 999,
    'algorithm': 'Kernel-GCNN',
    'num_neighbors': 99,
    'validation_loss': 0.9999,
    'rmse': 0.9999,
    'max_absolute_error': 0.9999,
    'r2_score': 0.9999
  },
  labels: ['label1', 'label2', 'label3', 'label4', 'label5',
    'label6', 'label7', 'label8', 'label9', 'label10',
    'label11', 'label12', 'label13', 'label14', 'label15']
}
