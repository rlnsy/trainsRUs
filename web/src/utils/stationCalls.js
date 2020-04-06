import axios from 'axios'
import { baseUrl } from './constants'

async function getAllStations() {
    return await axios({
        method: 'get',
        url: baseUrl + '/station',
        params: {
            body: {}
        }
    }).catch(error => {throw error})
}

export default { getAllStations }