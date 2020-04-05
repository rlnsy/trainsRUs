import axios from 'axios'
import { baseUrl } from './constants.js'

const JSONheader = { 
    'content-type': 'application/json',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
 }

async function getSummary() {
    var days = ['S','M','T','W','Th','F','Sa'];
    var totalWorkers = 0
    var workingToday = 0
    var now = new Date();
    var day = days[ now.getDay() ];
    const allWorkers = await this.getAllWorkers()

    totalWorkers = allWorkers.length
    workingToday = allWorkers.filter(w => w.availability.split(' ').includes(day)).length

    return {
        totalWorkers: totalWorkers,
        workingToday: workingToday,
    }
}

async function getAllWorkers() {
    const url = baseUrl + '/worker'
    axios({
        method: 'GET',
        url: url,
    }).then((response) => {
        return response
    }, (error) => {
        throw error
    })
}

async function getWorker(formData) {
    const url = baseUrl + '/worker'
    const request = {}
    request.workerId = Number(formData.id)
    const requestData = JSON.stringify(request)
    axios({
        method: 'GET',
        url: url,
        params: {
            'body': requestData
        },
    }).then((response) => {
        return response
    }, (error) => {
        throw error
    })
}

async function createWorker(formData) {
    axios({
        method: 'post',
        url: baseUrl + '/worker',
        headers: JSONheader,
        data: JSON.stringify(formData),
      }).then((response) => {
          return response
      }, (error) => {
          throw error
      })
}

async function deleteWorker(formData) {
    axios({
        method: 'delete',
        url: baseUrl + '/worker',
        headers: JSONheader,
        data: JSON.stringify(formData)
      }).then((response) => {
          return response
      }, (error) => {
          throw error
      })
}

export default { getSummary, getAllWorkers, getWorker, createWorker, deleteWorker }