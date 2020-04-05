export const baseUrl = "http://localhost:5000/v1"

export const Departments = {
    STATION: 'Station',
    TRACK: 'Maintenance',
    TRAIN: 'Train'
}

export const Conditions = {
    GOOD: 'Normal',
    REPAIRS: 'Needs Repairs',
    CRITICAL: 'Critical',
}

export const JSONheader = { 
    'content-type': 'application/json',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
 }