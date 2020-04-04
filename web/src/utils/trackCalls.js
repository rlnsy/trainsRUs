import axios from 'axios'

async function getSummary() {
    return {
        totalTracks: 14,
        needRepairs: 3,
        criticalCondition: 1,
    }
}

async function getAllTracks(cond) {
    return [
        {
            segmentID: 'ts2',
            startStation: 'Central Station',
            endStation: 'East Station',
            condition: 'Normal',
            length: 330,
        },
        {
            segmentID: 'ts673',
            startStation: 'Lake Port Station',
            endStation: 'Vancouver Station',
            condition: 'Critical',
            length: 1000,
        },
        {
            segmentID: 'ts3215',
            startStation: 'Townsville Station',
            endStation: 'Central Station',
            condition: 'Needs Repair',
            length: 660,
        },
    ].filter(t => cond === '' ? true : t.condition === cond)
}

export default { getSummary, getAllTracks }