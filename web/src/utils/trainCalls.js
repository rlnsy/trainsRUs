import axios from 'axios'
import { baseUrl } from './constants.js'

async function getSummary(id) {
    const all = await this.allShifts(id)
    const total = all.length
    const tripIDSet = Set()
    all.forEach(shift => tripIDSet.add(shift.tripId))
    return {
        upcomingShifts: total,
        distinctTrips: tripIDSet.size(),
    }
}

async function getShifts(id) {
    const url = baseUrl + '/shift'
    const request = {}
    request.workerId = Number(id)
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

async function getTicketInfo(formData) {
    axios({
        method: 'get',
        url: baseUrl + "/ticket/info",
        params: {
            'body': JSON.stringify(formData)
        },
    }).then((response) => {
        response.valid = true;
        return response
    }, (error) => {
        throw error
    })
}

export default { getSummary, getShifts, getTicketInfo}