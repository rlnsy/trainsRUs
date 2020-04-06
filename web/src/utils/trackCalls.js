import axios from 'axios'
import { baseUrl, JSONheader, Conditions} from './constants.js'

async function getSummary() {
    const goodCount = await getStats(Conditions.GOOD)
    const repairCount = await getStats(Conditions.REPAIRS)
    const criticalCount = await getStats(Conditions.CRITICAL)

    return {
        totalTracks: goodCount.data.numSegments + repairCount.data.numSegments + criticalCount.data.numSegments,
        needRepairs: repairCount.data.numSegments,
        criticalCondition: criticalCount.data.numSegments,
    }
}

async function getStats(status){
    return await axios({
        method: 'GET',
        url: baseUrl + '/segment/status/count',
        params: {
            'body': JSON.stringify({
                'status': status
            })
        },
    }).catch(error => {
        throw error
    })
}

async function getAllTracks(cond) {
    if(cond){ 
        return await axios({
            method: 'GET',
            url: baseUrl + '/segment',
            params: {
                'body': JSON.stringify({
                    'condition': cond
                })
            },
        }).catch(error => {
            throw error
        })
    } else {
        return await axios({
            method: 'GET',
            url: baseUrl + '/segment/status',
            params: {
                'body': '{}'
            }
        }).catch(error => {
            throw error
        })
    }
}

async function updateSegment(formData){
    console.log(formData)
    return await axios({
        method: 'PUT',
        url: baseUrl + '/segment/status',
        headers: JSONheader,
        data: JSON.stringify(formData)
    }).catch(error => {
        throw error
    })
}

export default { getSummary, getAllTracks, updateSegment }