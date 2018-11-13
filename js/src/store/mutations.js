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
      // if (m['state'] === 0) {
      //   state.model_counts_per_algorith['Reserved'] += 1
      // } else if (m['state'] === 1) {
      //   state.model_counts_per_algorith['Running'] += 1
      // } else {

      if (m['algorithm'] === 0) {
        state.model_counts_per_algorith['C-GCNN'] += 1
      } else if (m['algorithm'] === 1) {
        state.model_counts_per_algorith['Kernel-GCNN'] += 1
      } else if (m['algorithm'] === 2) {
        state.model_counts_per_algorith['DBSCAN-GCNN'] += 1
      }
      // }

      // set deployed model
      if (m['deployed'] === 1) {
        state.deployed_model_id = m.model_id
      }
    }

    // default select last model
    if (payload.model_list.length > 0 && !state.selected_model_id) {
      state.selected_model_id = payload.model_list[0].model_id
    }
  },

  // set sort key
  setSortKey (state, payload) {
    state.sort_key = payload.sort_key
  },

  /**
  * Model Detail
  */
  // set selected model_id
  setSelectedModelId (state, payload) {
    state.selected_model_id = payload.model_id
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
    state.dataset_list = payload.datasets
  },

  /**
  * prediction
  */
  setPredResult (state, payload) {
    state.pred_x = payload.data.pred_x
    state.pred_y = payload.data.pred_y
  }
}
