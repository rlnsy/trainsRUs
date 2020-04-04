import axios from 'axios'
import { baseUrl } from './constants.js'

async function getSummary(id) {
    return {
        upcomingShifts: 14,
        distinctTrips: 3,
    }
}

async function getShifts(id) {
    return [
        {
            tripID: 't321',
            segmentID: 's123',
            startStation: 'Central Station',
            endStation: 'East Station',
        },
        {
            tripID: 't321',
            segmentID: 's123',
            startStation: 'Central Station',
            endStation: 'East Station',
        },
        {
            tripID: 't321',
            segmentID: 's123',
            startStation: 'Central Station',
            endStation: 'East Station',
        },
    ]
}

async function getTicketInfo(IDs) {
    axios({
        method: 'get',
        url: baseUrl + "ticket/info",
        data: {
            tripID: IDs.tripID,
            ticketID: IDs.ticketID
        }
    }).then((response) => {
        response.valid = true;
        return response
    }, (error) => {
        throw error
    })
}

export default { getSummary, getShifts, getTicketInfo}