import axios from 'axios'
import { baseUrl } from './constants.js'

async function getSummary(id) {
    const response = await this.getShifts(id)
    const all = response.data
    const total = all.length
    const tripIDSet = new Set()
    all.forEach(shift => tripIDSet.add(shift.tripId))
    return {
        upcomingShifts: total,
        distinctTrips: tripIDSet.size,
    }
}

async function getShifts(id) {
    const request = {}
    request.workerId = Number(id)
    const requestData = JSON.stringify(request)
    return await axios({
        method: 'GET',
        url: baseUrl + '/shift',
        params: {
            'body': requestData
        },
    }).catch(error => {
        throw error
    })
}

async function getTicketInfo(formData) {
    return await axios({
        method: 'get',
        url: baseUrl + "/ticket/info",
        params: {
            'body': JSON.stringify(formData)
        },
    }).catch(error => {
        throw error
    })
}

export default { getSummary, getShifts, getTicketInfo}