import axios from 'axios'
import { baseUrl, JSONheader } from './constants.js'



async function getSummary() {
    var days = ['Su','M','T','W','Th','F','Sa'];
    var now = new Date();
    var day = days[ now.getDay() ];
    var response = await this.getAllWorkers()
    var allWorkers = response.data
    var totalWorkers = allWorkers.length
    var workingToday  = allWorkers.filter(w => w.availability.split(' ').includes(day))

    return {
        totalWorkers: totalWorkers,
        workingToday: workingToday.length,
    }
}

async function getColumns(){
    const response = await this.getAllWorkers()
    return Object.keys(response.data[0])
}

async function getAllWorkers(columns) {
    const url = baseUrl + '/worker'
    return await axios({
        method: 'GET',
        url: url,
        params: {
            'body': {
                'fields': columns
            }
        }
    }).catch(error => {
        throw error
    })
}

async function getWorker(formData) {
    const url = baseUrl + '/worker'
    return await axios({
        method: 'GET',
        url: url,
        params: {
            'body': JSON.stringify(formData)
        },
    }).catch(error => {
        throw error
    })
}

async function createWorker(formData) {
    return await axios({
        method: 'post',
        url: baseUrl + '/worker',
        headers: JSONheader,
        data: JSON.stringify(formData),
      }).catch(error => {
        throw error
    })
}

async function deleteWorker(formData) {
    return await axios({
        method: 'delete',
        url: baseUrl + '/worker',
        headers: JSONheader,
        data: JSON.stringify(formData)
      }).catch(error => {
        throw error
    })
}

async function getOverworked(){ 
    return await axios({
        method: 'GET',
        url: baseUrl + '/worker/overworked',
        params: {
            'body': {}
        },
    }).catch(error => {
        throw error
    })
}

export default { getSummary, getAllWorkers, getWorker, createWorker, deleteWorker, getColumns, getOverworked }