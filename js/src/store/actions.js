import axios from 'axios'

export default {
  loadLabels (context, payload) {
    const url = '/api/renom_rg/datasets/labels'
    axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
          return
        }

        context.commit('setLabels', {
          'labels': response.data.labels
        })
      })
  },

  async loadModels (context, payload) {
    const url = '/api/renom_rg/models'
    return axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
          return
        }

        context.commit('setModelList', {
          'model_list': response.data.models
        })
      })
  },

  async createModel (context, payload) {
    let fd = new FormData()
    fd.append('dataset_id', payload.dataset_id)
    fd.append('algorithm', payload.algorithm)
    fd.append('algorithm_params', JSON.stringify(payload.algorithm_params))
    fd.append('batch_size', payload.batch_size)
    fd.append('epoch', payload.epoch)

    const url = '/api/renom_rg/models'
    return axios.post(url, fd)
  },

  async runModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/train'
    return axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
        }
      })
  },

  async addModel (context, payload) {
    const result = await context.dispatch('createModel', payload)
    if (result.data.error_msg) {
      context.commit('setErrorMsg', {'error_msg': result.data.error_msg})
      return
    }

    const model_id = result.data.model_id
    await context.dispatch('runModel', {'model_id': model_id})
    if (result.data.error_msg) {
      context.commit('setErrorMsg', {'error_msg': result.data.error_msg})
      return
    }

    await context.dispatch('loadModels')
  },

  async deleteModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id
    return axios.delete(url)
  },

  async deleteAndUpdate (context, payload) {
    await context.dispatch('deleteModel', payload)
    await context.dispatch('loadModels')
  },

  async selectModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id
    axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
          return
        }

        context.commit('setSelectedModelId', payload)
        context.commit('setSelectedModel', {'model': response.data.model})
        context.commit('setSelectedYValid', {'selected_y_valid': response.data.model.selected_y_valid})
        context.commit('setSelectedYPred', {'selected_y_pred': response.data.model.selected_y_pred})
      })
  },

  async deployModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/deploy'
    return axios.post(url)
  },

  async undeployModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/undeploy'
    return axios.post(url)
  },

  async deployAndUpdate (context, payload) {
    await context.dispatch('deployModel', payload)
    await context.dispatch('loadModels')
    await context.dispatch('selectModel', payload)
  },

  async undeployAndUpdate (context, payload) {
    await context.dispatch('undeployModel', payload)
    await context.dispatch('loadModels')
    await context.dispatch('selectModel', payload)
  },

  loadDatasets (context, payload) {
    const url = '/api/renom_rg/datasets'
    axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
          return
        }

        context.commit('setDatasets', {
          'datasets': response.data.datasets
        })
      })
  },

  confirmDataset (context, payload) {
    let fd = new FormData()
    fd.append('name', payload.name)
    fd.append('description', payload.description)
    fd.append('train_ratio', payload.train_ratio)
    fd.append('target_column_id', payload.target_column_id)

    const url = '/api/renom_rg/datasets/confirm'
    return axios.post(url, fd)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
          return
        }
        context.commit('setTrainCount', {'train_count': response.data.train_count})
        context.commit('setValidCount', {'valid_count': response.data.valid_count})
        context.commit('setTargetTrain', {'target_train': response.data.target_train})
        context.commit('setTargetValid', {'target_valid': response.data.target_valid})
        context.commit('setTrainIndex', {'train_index': response.data.train_index})
        context.commit('setValidIndex', {'valid_index': response.data.valid_index})
      })
  },

  saveDataset (context, payload) {
    let fd = new FormData()
    fd.append('name', payload.name)
    fd.append('description', payload.description)
    fd.append('train_ratio', payload.train_ratio)
    fd.append('target_column_id', payload.target_column_id)
    fd.append('labels', JSON.stringify(context.state.labels))
    fd.append('train_index', JSON.stringify(context.state.train_index))
    fd.append('valid_index', JSON.stringify(context.state.valid_index))

    const url = '/api/renom_rg/datasets'
    return axios.post(url, fd)
      .then(function (response) {
        if (response.data.error_msg) {
          context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
        }
      })
  }

  // runPrediction (context, payload) {
  //   const url = '/api/renom_rg/models/' + payload.model_id + '/predict'
  //   axios.get(url)
  //     .then(function (response) {
  //       if (response.data.error_msg) {
  //         context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
  //         return
  //       }
  //       console.log(response.data)
  //       // context.commit('setDeployedModel', {'model': response.data.model})
  //     })
  // }
}
