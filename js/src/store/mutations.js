export default {
  // set header page name
  setPageName (state, payload) {
    state.page_name = payload.page_name
  },

  setErrorMsg (state, payload) {
    state.error_msg = payload.error_msg
  },

  // show nav bar
  setNavigationBarShowFlag (state, payload) {
    state.navigation_bar_shown_flag = payload.flag
  },

  // set add model modal
  setAddModelModalShowFlag (state, payload) {
    state.add_model_modal_shown_flag = payload.flag
  },

  /**
  * dashboard
  */
  // add model count per algorithm
  addModelCount (state, payload) {
    state.model_counts_per_algorith[payload.algorithm] += 1
  },

  // add Running models
  addRunningModels (state, payload) {
    state.running_models[payload.model_id] = payload.model
  },

  /**
  * Model list
  */
  // set  mode llist
  setModelList (state, payload) {
    state.model_list = []
    state.model_counts_per_algorith = { 'C-GCNN': 0, 'Kernel-GCNN': 0, 'DBSCAN-GCNN': 0, 'Running': 0, 'Reserved': 0 }
    for (let m of payload.model_list) {
      state.model_list.push(m)

      // count models per algorithm
      if (m['state'] === 0) {
        state.model_counts_per_algorith['Reserved'] += 1
      } else if (m['state'] === 1) {
        state.model_counts_per_algorith['Running'] += 1
      } else {
        if (m['algorithm'] === 0) {
          state.model_counts_per_algorith['C-GCNN'] += 1
        } else if (m['algorithm'] === 1) {
          state.model_counts_per_algorith['Kernel-GCNN'] += 1
        } else if (m['algorithm'] === 0) {
          state.model_counts_per_algorith['DBSCAN-GCNN'] += 1
        }
      }

      // set deployed model
      if (m['deployed'] === 1) {
        state.deployed_model_id = m.model_id
      }
    }

    // default select last model
    if (!state.selected_model_id) {
      state.selected_model_id = payload.model_list[0].model_id
    }
  },

  // set sort key
  setSortKey (state, payload) {
    state.sort_key = payload.sort_key
  },

  // set deployed model
  setDeployedModelId (state, payload) {
    state.deployed_model_id = payload.deployed_model_id
  },

  /**
  * Model Detail
  */
  // set selected model_id
  setSelectedModelId (state, payload) {
    state.selected_model_id = payload.model_id
  },

  // set selected model
  setSelectedModel (state, payload) {
    state.selected_model = payload.model
    state.valid_loss_list = payload.model.valid_loss_list
    state.train_loss_list = payload.model.train_loss_list
    state.selected_y_valid = payload.model.valid_true
    state.selected_y_pred = payload.model.valid_predicted
  },

  updateDeployModel (state, payload) {
    state.deployed_model_id = state.selected_model_id
    state.deployed_model_y_valid = state.selected_y_valid
    state.deployed_model_y_pred = state.selected_y_pred
  },

  setDeployededModel (state, payload) {
    state.deployed_model_id = payload.model.model_id
    state.deployed_model_y_valid = payload.model.valid_true
    state.deployed_model_y_pred = payload.model.valid_predicted
    state.deployed_model = payload.model
  },

  /**
  * prediction sample
  */
  // set validation true data
  setDeployedYValid (state, payload) {
    state.deployed_y_valid = payload.deployed_y_valid
  },
  setDeployedYPred (state, payload) {
    state.deployed_y_pred = payload.deployed_y_pred
  },

  // set labels
  setLabels (state, payload) {
    state.labels = payload.labels
  },

  /**
  * mdoal
  */
  setConfirmDataset (state, payload) {
    state.train_count = payload.data.train_count
    state.valid_count = payload.data.valid_count
    state.target_train = payload.data.target_train
    state.target_valid = payload.data.target_valid
    state.train_index = payload.data.train_index
    state.valid_index = payload.data.valid_index
  },

  setDatasetList (state, payload) {
    state.dataset_name_list = []
    for (let d of payload.datasets) {
      state.dataset_name_list.push(d['name'])
    }
    state.dataset_list = payload.datasets
  },

  /**
  * dataset page
  */
  setSelectedDataset (state, payload) {
    state.selected_dataset_id = payload.dataset.dataset_id
    state.selected_dataset = payload.dataset
  }
}
