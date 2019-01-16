import axios from 'axios'

const commitError = function (context, error) {
  context.commit('setErrorMsg', { 'error_msg': error.response.data.err })
}

export default {
  async loadLabels (context, payload) {
    const url = '/api/renom_rg/datasets/labels'
    return axios.get(url)
      .then(function (response) {
        context.commit('setLabels', {
          'labels': response.data.labels
        })
      }).catch(function (error) { commitError(context, error) })
  },
  async loadModels (context, payload) {
    await context.dispatch('loadModelList')
  },

  async loadModelList (context, payload) {
    const url = '/api/renom_rg/models'
    return axios.get(url)
      .then(function (response) {
        context.commit('setModelList', {
          'model_list': response.data.models
        })
      }).catch(function (error) { commitError(context, error) })
  },

  async createModel (context, payload) {
    let fd = new FormData()
    fd.append('dataset_id', context.state.dataset_list[payload.dataset_index]['dataset_id'])
    fd.append('algorithm', payload.algorithm)
    fd.append('algorithm_params', JSON.stringify(payload.algorithm_params))
    fd.append('batch_size', payload.batch_size)
    fd.append('epoch', payload.epoch)

    const url = '/api/renom_rg/models'
    return axios.post(url, fd).catch(function (error) { commitError(context, error) })
  },

  async runModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/train'
    return axios.get(url).catch(function (error) { commitError(context, error) })
  },

  async addModel (context, payload) {
    let response = await context.dispatch('createModel', payload)

    const model_id = response.data.model_id
    await context.dispatch('runModel', { 'model_id': model_id })
    await context.dispatch('loadModelList')
  },

  loadRunningModels (context, payload) {
    const url = '/api/renom_rg/models/running'
    axios.get(url)
      .then(function (response) {
        for (let i in response.data.running_models) {
          if (context.state.running_models.length === 0 || response.data.running_models[i].nth_epoch > context.state.running_models[i].nth_epoch) {
            context.dispatch('loadModelList')
          }
        }
        context.commit('setRunningModels', { 'running_models': response.data.running_models })
      }).catch(function (error) {
        commitError(context, error)
      })
  },

  stopModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/stop'
    axios.get(url).catch(function (error) { commitError(context, error) })
  },

  async deleteModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id
    return axios.delete(url).catch(function (error) { commitError(context, error) })
  },

  async deleteAndUpdate (context, payload) {
    await context.dispatch('deleteModel', payload)
    await context.dispatch('loadModels')
  },

  async deployModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/deploy'
    return axios.post(url).catch(function (error) { commitError(context, error) })
  },

  async undeployModel (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/undeploy'
    return axios.post(url).catch(function (error) { commitError(context, error) })
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
        context.commit('setDatasetList', {
          'datasets': response.data.datasets
        })
      }).catch(function (error) {
        commitError(context, error)
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
        context.commit('setConfirmDataset', { 'data': response.data })
      }).catch(function (error) {
        commitError(context, error)
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
    fd.append('true_histogram', JSON.stringify(context.state.true_histogram))

    const url = '/api/renom_rg/datasets'
    return axios.post(url, fd)
      .catch(function (error) { commitError(context, error) })
  },

  async saveAndUpdateDataset (context, payload) {
    await context.dispatch('saveDataset', payload)
    await context.dispatch('loadDatasets')
  },

  runPrediction (context, payload) {
    const url = '/api/renom_rg/models/' + payload.model_id + '/predict'
    axios.get(url)
      .then(function (response) {
        context.commit('setPredResult', { 'data': response.data })
      }).catch(function (error) {
        commitError(context, error)
      })
  }
}
