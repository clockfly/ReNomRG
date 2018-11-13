export default {
  deployedModel: function (state) {
    return state.model_list.filter(model => model.deployed === 1)[0]
  },
  selectedModel: function (state) {
    return state.model_list.filter(model => model.model_id === state.selected_model_id)[0]
  },
  selectedDataset: function (state, getters) {
    if (!getters.selectedModel) return {}
    const selected_dataset_id = getters.selectedModel.dataset_id
    return state.dataset_list.filter(dataset => dataset.dataset_id === selected_dataset_id)[0]
  }
}
