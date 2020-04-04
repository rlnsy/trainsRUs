import axios from 'axios'

async function getAllStations(cond) {
    return [
        {
            sname: 'SF Station',
            location: 'Mountain View',
            capacity: '111',
        },
        {
            sname: 'East Station',
            location: 'East Capital',
            capacity: '3131',
        },
        {
            sname: 'Central Station',
            location: 'Central City',
            capacity: '100',
        },
    ]
}

export default { getAllStations }