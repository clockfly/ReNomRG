import axios from 'axios'

const commitError = function (context, response) {
  context.commit('setErrorMsg', {'error_msg': response.data.error_msg})
}

export default {
  async loadLabels (context, payload) {
    const url = '/api/renom_rg/datasets/labels'
    return axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setLabels', {
          'labels': response.data.labels
        })
      })
  },
  async loadModels (context, payload) {
    await context.dispatch('loadModelList')
  },

  async loadModelList (context, payload) {
    const url = '/api/renom_rg/models'
    return axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setModelList', {
          'model_list': response.data.models
        })
      })
  },

  async createModel (context, payload) {
    let fd = new FormData()
    fd.append('dataset_id', context.state.dataset_list[payload.dataset_index]['dataset_id'])
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
          commitError(context, response)
        }
      })
  },

  async addModel (context, payload) {
    let response = await context.dispatch('createModel', payload)
    if (response.data.error_msg) {
      commitError(context, response)
      return
    }
    const model_id = response.data.model_id
    response = await context.dispatch('runModel', {'model_id': model_id})
    if (response.data.error_msg) {
      commitError(context, response)
      return
    }

    await context.dispatch('loadModelList')
  },

  loadRunningModels (context, payload) {
    const url = '/api/renom_rg/models/running'
    axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setRunningModels', {'running_models': response.data.running_models})
      })
  },

  async deleteModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id
    return axios.delete(url)
  },

  async deleteAndUpdate (context, payload) {
    await context.dispatch('deleteModel', payload)
    await context.dispatch('loadModels')
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
  },

  async undeployAndUpdate (context, payload) {
    await context.dispatch('undeployModel', payload)
    await context.dispatch('loadModels')
  },

  async loadDatasets (context, payload) {
    const url = '/api/renom_rg/datasets'
    return axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setDatasetList', {
          'datasets': response.data.datasets
        })
      })
  },

  confirmDataset (context, payload) {
    let fd = new FormData()
    fd.append('name', payload.name)
    fd.append('description', payload.description)
    fd.append('train_ratio', payload.train_ratio)
    fd.append('target_column_ids', JSON.stringify(payload.target_column_ids))

    const url = '/api/renom_rg/datasets/confirm'
    return axios.post(url, fd)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setConfirmDataset', { 'data': response.data })
      })
  },

  async saveDataset (context, payload) {
    let fd = new FormData()
    fd.append('name', payload.name)
    fd.append('description', payload.description)
    fd.append('train_ratio', payload.train_ratio)
    fd.append('target_column_ids', JSON.stringify(payload.target_column_ids))
    fd.append('labels', JSON.stringify(context.state.labels))
    fd.append('train_index', JSON.stringify(context.state.train_index))
    fd.append('valid_index', JSON.stringify(context.state.valid_index))
    fd.append('target_train', JSON.stringify(context.state.target_train))
    fd.append('target_valid', JSON.stringify(context.state.target_valid))

    const url = '/api/renom_rg/datasets'
    return axios.post(url, fd)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
        }
      })
  },

  async saveAndUpdateDataset (context, payload) {
    await context.dispatch('saveDataset', payload)
    await context.dispatch('loadDatasets')
  },

  runPrediction (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/predict'
    axios.get(url)
      .then(function (response) {
        if (response.data.error_msg) {
          commitError(context, response)
          return
        }
        context.commit('setPredResult', {'data': response.data})
      })
  }
}
