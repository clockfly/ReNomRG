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
    fd.append('batch_size', payload.epoch)

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
