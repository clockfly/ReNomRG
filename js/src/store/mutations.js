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
    for (let m of payload.model_list) {
      state.model_list.push(m)
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
    }

    // TODO: select last model if selected_model_id is undefined
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
  },

  /**
  * prediction sample
  */
  // set validation true data
  setSelectedYValid (state, payload) {
    state.selected_y_valid = payload.selected_y_valid
  },
  setSelectedYPred (state, payload) {
    state.selected_y_pred = payload.selected_y_pred
  },
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
  setTrainCount (state, payload) {
    state.train_count = payload.train_count
  },
  setValidCount (state, payload) {
    state.valid_count = payload.valid_count
  },
  setTargetTrain (state, payload) {
    state.target_train = payload.target_train
  },
  setTargetValid (state, payload) {
    state.target_valid = payload.target_valid
  },
  setTrainIndex (state, payload) {
    state.train_index = payload.train_index
  },
  setValidIndex (state, payload) {
    state.valid_index = payload.valid_index
  }
}
