import axios from 'axios'

async function getSummary() {
    return {
        totalWorkers: 35,
        workingToday: 14
    }
}

async function getAllWorkers() {
    return [
        {
            id: 'w3217841',
            firstName: 'John',
            lastName: 'Smith',
            role: 'Salesperson',
            type: 'Station',
            phoneNumber: '1113215231',
            availability: 'M W Th F',
        },
        {
            id: 'w4571023',
            firstName: 'Jane',
            lastName: 'Doe',
            role: 'Engineer',
            type: 'Maintenance',
            phoneNumber: '2225634213',
            availability: 'M T W',
        },
        {
            id: 'w58728937',
            firstName: 'James',
            lastName: 'Lee',
            role: 'Ticket Collector',
            type: 'Train',
            phoneNumber: '3330983215',
            availability: 'M F Sa S',
        },
    ]
}

export default { getSummary, getAllWorkers }