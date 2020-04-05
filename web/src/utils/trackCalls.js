import axios from 'axios'
import { baseUrl, JSONheader, Conditions} from './constants.js'

async function getSummary() {
    const goodCount = await getStats(Conditions.GOOD).numSegments
    const repairCount = await getStats(Conditions.REPAIRS).numSegments
    const criticalCount = await getStats(Conditions.CRITICAL).numSegments

    return {
        totalTracks: goodCount + repairCount + criticalCount,
        needRepairs: repairCount,
        criticalCondition: criticalCount,
    }
}

async function getStats(status){
    axios({
        method: 'GET',
        url: baseUrl + '/segment/status/count',
        params: {
            'body': JSON.stringify({
                'status': status
            })
        },
    }).then((response) => {
        return response
    }, (error) => {
        throw error
    })
}

async function getAllTracks(cond) {
    if(cond){ 
        axios({
            method: 'GET',
            url: baseUrl + '/segment',
            params: {
                'body': JSON.stringify({
                    'condition': cond
                })
            },
        }).then((response) => {
            return response
        }, (error) => {
            throw error
        })
    } else {
        axios({
            method: 'GET',
            url: baseUrl + '/segment/status',
        }).then((response) => {
            return response
        }, (error) => {
            throw error
        })
    }
}

async function updateSegment(formData){
    axios({
        method: 'PUT',
        url: baseUrl + '/segment/status',
        headers: JSONheader,
        data: JSON.stringify(formData)
    }).then((response) => {
        return response
    }, (error) => {
        throw error
    })
}

export default { getSummary, getAllTracks, updateSegment }